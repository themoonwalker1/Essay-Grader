from __future__ import absolute_import, unicode_literals
from essay_grader.celery import app
import os
import sys
from .citation import *
from grammarbot import GrammarBotClient
from .models import Essay
import unidecode
    
@app.task(trail=True)
def grade_all(essay_ids) -> list:
    return [grade_essay(essay_id) for essay_id in essay_ids]


@app.task(trail=True)
def grade_essay(essay_id) -> tuple:
    essay = Essay.objects.get(id=essay_id)
    client = GrammarBotClient()
    edited_body = ""
    cursor = 0
    citation_heading = ""

    if essay.citation_type == "APA":
        citation_heading = "References"
    else:
        citation_heading = "Works Cited"

    if citation_heading not in essay.raw_body:
        ret = "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">" + "ERROR: No reference list/works cited header found (this may be due to a typo in the word \"References\" or the word \"Works Cited\"). Unable to mark essay." + "</mark></p>" + essay.raw_body
        return essay_id, ret

    body = check_citations(essay_id)

    body = body.split(citation_heading)
    raw_citations = "<p>" + citation_heading + "</p>" + body[-1]
    body = citation_heading.join(body[:-1])
    result = client.check(body)

    for match in result.matches:  # you also have access to match.category if you want
        offset = match.replacement_offset
        length = match.replacement_length

        edited_body += body[cursor:offset]
        edited_body += "<mark style=\"background-color:red;\">" + body[offset:(offset + length)] + "</mark>"
        cursor = offset + length

        # if cursor < text length, then add remaining text to new_text
        if cursor >= len(body):
            edited_body += body[cursor:]
            
    if edited_body == "":
        edited_body = body

    edited_body += raw_citations
    return essay_id, edited_body

@app.task(trail=True)
def check_citations(essay_id):
    essay = Essay.objects.get(id=essay_id)
    citation_type = essay.citation_type
    citation_heading = ""

    if citation_type == "APA":
        citation_heading = "References"
    else:
        citation_heading = "Works Cited"

    body = essay.raw_body.split(citation_heading)
    raw_citations = body[-1].splitlines()
    body = body[:-1]
    body = [citation_heading.join(body)]
    body.append(citation_heading)
    raw_citations = list(filter(None, [i.strip() for i in raw_citations]))
    citations = []

    for i in raw_citations:
        citation = None
        
        if citation_type == "APA":
            citation = APACitation()
        else:
            citation = MLACitation()

        try:
            citation.check_citation(i)
        except Exception as e:
            body.append(
                cross_reference(citation, citation_type, body[0]) + 
                "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR (in the " + citation.citation_status.value + " section): " + 
                str(e) + "</mark></p>" +
                "<p><mark style=\"background-color:red;line-height:1.5em\">" + i + "</mark></p>"
                )
        else:
            citation.warnings = list(filter(None, [i.strip() for i in citation.warnings]))
            if citation.warnings != []:
                body.append(
                    cross_reference(citation, citation_type, body[0]) +
                    "<p style=\"padding-top:1em\"><mark style=\"background-color:yellow;line-height:1.5em\">WARNING: " + str(citation.warnings)[1:-1] + "</p>" + 
                    "<p><mark style=\"background-color:yellow;line-height:1.5em\">" + i + "</mark></p>"
                    )
            else:
                body.append(
                    cross_reference(citation, citation_type, body[0]) +
                    "<p><mark style=\"background-color:green;line-height:1.5em\">"+ i + "</mark></p>"
                    )
        finally:
            citations.append(citation)
            continue

    for i in range(len(citations) - 1):
        if citations[i].authors != [] and citations[i + 1].authors != []:
            firstAuthor = unidecode.unidecode(citations[i].authors[0])
            secondAuthor = unidecode.unidecode(citations[i + 1].authors[0])
            if firstAuthor > secondAuthor:
                body.insert(1, 
                "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">" + 
                "ERROR: Citations are not arranged alphabetically." + 
                "</mark></p>"
                )
                break
    
    return "\n".join(body)

@app.task(trail=True)
def cross_reference(citation, citation_type, body):
    if citation_type == "APA":
        if citation.citation_status != APACitationStatus.AUTHOR and citation.citation_status != APACitationStatus.YEAR:
            if len(citation.authors) == 1:
                author_count = body.count(citation.authors[0])
                year_count = body.count(citation.year)
                total = min(author_count, year_count)

                if total == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(total) + ". </mark></p>"
            
            elif len(citation.authors) == 2:
                author_1 = " & ".join(citation.authors)
                author_2 = " and ".join(citation.authors)
                author_count = body.count(author_1) + body.count(author_2)
                year_count = body.count(citation.year)
                total = min(author_count, year_count)

                if total == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(total) + ". </mark></p>"
            
            else:
                author = citation.authors[0] + " et al."
                author_count = body.count(author)
                year_count = body.count(citation.year)
                total = min(author_count, year_count)

                if total == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(total) + ". </mark></p>"
        else:
            return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: Invalid citation; unable to cross-reference. </mark></p>"

    else:
        if citation.citation_status != MLACitationStatus.AUTHOR:
            if len(citation.authors) == 1:
                author_count = body.count(citation.authors[0])

                if author_count == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(author_count) + ". </mark></p>"
            
            elif len(citation.authors) == 2:
                author_count = body.count(" and ".join(citation.authors))

                if author_count == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(author_count) + ". </mark></p>"
            
            else:
                author_count = body.count(citation.authors[0] + " et al.")

                if author_count == 0:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: No in-text citations found for this citation. </mark></p>"
                else:
                    return "<p style=\"padding-top:1em\"><mark style=\"background-color:green;line-height:1.5em\">Number of in-text occurrences found in the essay: " + str(author_count) + ". </mark></p>"
        else:
            return "<p style=\"padding-top:1em\"><mark style=\"background-color:red;line-height:1.5em\">ERROR: Invalid citation; unable to cross-reference. </mark></p>"

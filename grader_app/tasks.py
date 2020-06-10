from __future__ import absolute_import, unicode_literals
from essay_grader.celery import app
import os
import sys
from .citation import *
from grammarbot import GrammarBotClient
from .models import Essay
    
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
        ret = "<p><mark style=\"background-color:yellow;line-height:1.5em\">" + "ERROR: No reference list/works cited header found (this may be due to a typo in the word \"References\" or the word \"Works Cited\"). Unable to mark essay." + "</mark></p>" + essay.raw_body
        return essay_id, ret

    body = check_citations(essay_id)

    body = body.split(citation_heading)
    raw_citations = citation_heading + body[-1]
    body = citation_heading.join(body[:-1])

    result = client.check(body)

    for match in result.matches:  # you also have access to match.category if you want
        offset = match.replacement_offset
        length = match.replacement_length

        edited_body += body[cursor:offset]
        edited_body += "<mark style=\"background-color:yellow;\">" + body[offset:(offset + length)] + "</mark>"
        cursor = offset + length

        # if cursor < text length, then add remaining text to new_text
        if cursor >= len(body):
            edited_body += body[cursor:]
    if edited_body == "":
        edited_body = essay.marked_body
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
                "<p><mark style=\"background-color:yellow;line-height:1.5em\">ERROR (in the " + citation.citation_status.value + " section): </p>" + 
                str(e) +
                "<p><mark style=\"background-color:yellow;line-height:1.5em\">" + i + "</mark></p>"
                )
        else:
            citation.warnings = list(filter(None, [i.strip() for i in citation.warnings]))
            if citation.warnings != []:
                body.append(
                    "<p><mark style=\"background-color:orange;line-height:1.5em\">WARNING: " + str(citation.warnings)[1:-1] + "</p>" + 
                    "<p><mark style=\"background-color:orange;line-height:1.5em\">" + i + "</mark></p>"
                    )
            else:
                body.append(i)
        finally:
            citations.append(citation)
            continue

    #cross referencing
    #build parenthetical citations, store them in a list
    #for each citation in citations (not parenthetical):
        #if citation doesnt have an error in the author or the year:   
            #check for entry in parenthetical
    
    #make a method to check if authors in a parenthetical match authors in a non-parenthetical citation
    
    return "\n".join(body)
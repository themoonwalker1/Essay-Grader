from __future__ import absolute_import, unicode_literals
from essay_grader.celery import app
import os
import sys
from .citation import *
from grammarbot import GrammarBotClient
from .models import Essay

@app.task()
def check_citations(essay_id):
    pass

@app.task(trail=True)
def grade_all(essay_ids) -> list:
    return [grade_essay(essay_id) for essay_id in essay_ids]


@app.task(trail=True)
def grade_essay(essay_id) -> tuple:
    essay = Essay.objects.get(id=essay_id)
    client = GrammarBotClient()
    edited_body = ""
    cursor = 0
    body = essay.body
    result = client.check(body)

    for match in result.matches:  # you also have access to match.category if you want
        offset = match.replacement_offset
        length = match.replacement_length

        edited_body += body[cursor:offset]
        edited_body += "<mark style=\"background-color:yellow;\"><b>" + body[offset:(offset + length)] + "</b></mark>"
        cursor = offset + length

        # if cursor < text length, then add remaining text to new_text
        if cursor >= len(body):
            edited_body += body[cursor:]
    if edited_body == "":
        edited_body = essay.marked_body
    return essay_id, edited_body

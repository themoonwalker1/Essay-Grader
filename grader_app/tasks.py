from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Essay
from grammarbot import GrammarBotClient
from .models import Essay

@shared_task
def grade_essay(id):
    essay = Essay.objects.get(id=id)
    client = GrammarBotClient()
    edited_body = ""
    cursor = 0
    body = essay.body
    result = client.check(body)
    
    for match in result.matches: #you also have access to match.category if you want
        offset = match.replacement_offset 
        length = match.replacement_length 

        if cursor > offset: 
            continue

        edited_body += body[cursor:offset]
        edited_body += "**" + body[offset:(offset + length)] + "**"
        cursor = offset + length
        
        # if cursor < text length, then add remaining text to new_text
        if cursor < len(body):
            edited_body += body[cursor:]
    if edited_body == "":
        edited_body = essay.body

    essay.graded = True
    essay.marked_body = edited_body
    essay.save()
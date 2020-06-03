from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Essay
from grammarbot import GrammarBotClient
from .models import Essay

@shared_task
def grade_essay(pk):
    print("Inside tasks")
    essay = Essay.objects.get(pk=pk)
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
    print("edited body:", edited_body)
    if edited_body == "":
        edited_body = reformat(essay.body)

    essay.graded = True
    essay.marked_body = edited_body
    essay.save()
    print(essay.graded)
    return essay.marked_body

def reformat(body):
    temp = body.split("\r\n")
    tempText = "<p>"

    for paragraph in temp:
        tempText += paragraph + "</p><p>"

    temp = tempText.split("\t")
    tempText = "&emsp;"

    for tab in temp:
        tempText += tab + "&emsp;"

    temp = ""
    for word in tempText.split(" "):
        if len(word) <= 4:
            temp += word + " "
        elif word[0:2] == "**":
            temp += "<mark style=\"background-color:yellow;\"><b>" + word[2:len(word) - 2] + "</b></mark> "
        else:
            temp += word + " "

    return temp + "</p>"
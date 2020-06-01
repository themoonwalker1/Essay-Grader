from django.shortcuts import render, redirect
from .models import Essay
from .forms import EssayForm, LoginForm, RegisterForm, SetupForm
from django.contrib.auth.decorators import login_required
from requests_oauthlib import OAuth2Session
from .models import User
from django.contrib import auth
from grammarbot import GrammarBotClient
from django.db.models import Q
from operator import attrgetter
from django import forms
import json

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {
        'url' : 'login'
    }

    CODE = None
    CLIENT_ID = "FeZBHle5SNytiEwAh333mPmoEmfFDQSF1Jigy2bW"
    CLIENT_SECRET = "saNPOvrrCGhNK1TywLjTsKo3M5uFzfQEgUtTpvvZsNIQPB75eeWYqhBxYMZJb0lKG5LZRZx1ZVN7ZUEiUUUqPeE8GMH0ZwdhbG4yNKKYmcCDu0UXV2gopeUB3B4cAIzw"
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email=form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                user = auth.authenticate(email=email, password=form.cleaned_data["password"])
                if user is not None:
                    auth.login(request, user)
                    return redirect("http://localhost:8000/home")
            else:
                form = LoginForm() 
                context['form'] = form
                
            context['error'] = "Username or Password is incorrect"

    else:
        form = LoginForm() 
        context['form'] = form
    if request.method == 'GET':
        oauth = OAuth2Session(CLIENT_ID,
                    redirect_uri="http://localhost:8000/login",
                    scope=["read"])
        authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
        context['url'] = authorization_url
        if "code" in request.GET:
            CODE = request.GET.get("code")
            
            token = oauth.fetch_token("https://ion.tjhsst.edu/oauth/token/",
                            code=CODE,
                            client_secret=CLIENT_SECRET)
            
            try:
                raw_profile = oauth.get("https://ion.tjhsst.edu/api/profile")
                profile = json.loads(raw_profile.content.decode())
                email = profile["tj_email"]
                if User.objects.filter(email=email).exists():
                    user = auth.authenticate(email=email, password=profile.get("ion_username") + profile.get("user_type"))
                    if user is not None:
                        auth.login(request, user)
                        return redirect("http://localhost:8000/home")
                else:
                    if profile.get("is_teacher"):
                        new_user = User.objects.create_teacheruser(email=email, password=profile.get("ion_username") + profile.get("user_type"))
                    else:
                        new_user = User.objects.create_studentuser(email=email, password=profile.get("ion_username") + profile.get("user_type"))
                    new_user.first_name = profile.get("first_name")
                    new_user.middle_name = profile.get("middle_name")
                    new_user.last_name = profile.get("last_name")
                    new_user.year_in_school = profile.get("grade").get("name").upper()[:3]
                    new_user.save()
                    user = auth.authenticate(email=email, password=profile.get("ion_username") + profile.get("user_type"))
                    auth.login(request, user)
                    return redirect("http://localhost:8000/home")

            except Exception as e:
                args = { "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET }
                token = oauth.refresh_token("https://ion.tjhsst.edu/oauth/token/", **args)
    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("login")
    
def create(request):    
    if request.user.is_authenticated:
        return redirect("home")
    context = {"method" : request.method}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            error = False
            try:
                email = form.cleaned_data.get('email')
                qs = User.objects.filter(email=email)
                if qs.exists():
                    raise forms.ValidationError("email is taken")
            except forms.ValidationError:
                context['Error1'] = "Email is already taken"
                error = True
                
            try:
                password = form.clean_password2()
                if len(password) < 8:
                    raise ValueError
            except forms.ValidationError:
                context['Error2'] = "Passwords do no match"
                error = True
            except ValueError:
                context['Error2'] = "Passwords need to be at least 8 characters"
                error = True
                
            if not error:
                new_user = User.objects.create_studentuser(email=email, password=password)
                new_user.save()

                user = auth.authenticate(email=email, password=password)
                auth.login(request, user)
                return redirect("http://localhost:8000/setup")
            else:
                form = RegisterForm()
                context['form'] = form
        else:
            form = RegisterForm()
            context['form'] = form
                
    else:
        form = RegisterForm()
        context['form'] = form
    return render(request, "create.html", context)
            
def setup(request) :
    context = {
        "method" : request.method,
        "form" : SetupForm()
    }
    if context['method'] == "POST":
        form = SetupForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.middle_name = form.cleaned_data.get('middle_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.year_in_school = form.cleaned_data.get('year_in_school')
            user.save()
            return redirect("home")
    return render(request, "setup.html", context)
    

@login_required(login_url="login")
def index(request):
    if (request.user.first_name == ""):
        return redirect("setup")
    essays = []
    query = ""
    if request.GET:
        query = request.GET.get('q', 'Search for an essay')

    if query != "":
        profile = request.user
        queryset = []
        queries = query.split(" ")

        for q in queries:
            essays = Essay.objects.filter(author=request.user).filter(
                    Q(assignment__icontains=q) |
                    Q(title__icontains=q) |
                    Q(body__icontains=q) |
                    Q(teacher__icontains=q)
            ).order_by('-created_on').distinct()

            for essay in essays:
                queryset.append(essay)
                
        essays =  list(set(queryset))
        
    if request.user.teacher or request.user.admin:
        return redirect("teacher")

    if essays == []:
        essays = Essay.objects.all().filter(author=request.user).order_by('-created_on')
    
    context = {
        "essays": essays,
        "query": str(query),
        "search": query != ""
    }
    
    return render(request, "index.html", context)
    
@login_required(login_url="login")
def submit(request):
    profile = request.user

    if request.method == 'POST':
        form = EssayForm(request.POST)

        if form.is_valid():
            essay = Essay(
                title=form.cleaned_data["title"],
                body=form.cleaned_data["body"],
                author=request.user,
                assignment=form.cleaned_data["assignment"],
                teacher=form.cleaned_data["teacher"],
                citation_type=form.cleaned_data["citation_type"]
            )
            essay.save()

            return redirect("home")

    else:
        form = EssayForm() 
        context = {
            'form': form,
        }
        return render(request, "submit.html", context)
        
@login_required(login_url="login")
def detail(request, pk):
    essay = Essay.objects.filter(email=request.user.email).get(pk=pk)
    context = {
        'essay': essay
    }

    return render(request, "detail.html", context)


@login_required(login_url="login")
def teacher(request):
    user = request.user

    if user.student:
        return redirect("http://localhost:8000/home")

    query = ""

    if request.GET:
        query=request.GET.get("q", "")
        queryset = []
        queries = query.split(" ")

        for q in queries:
            essays = Essay.objects.filter(teacher=user.email).filter(
                    Q(assignment__icontains=q) |
                    Q(title__icontains=q) |
                    Q(body__icontains=q) |
                    Q(teacher__icontains=q)
            ).order_by('-created_on').distinct()

            for essay in essays:
                queryset.append(essay)
                
        essays =  list(set(queryset))

    else:
        try:
            essays = Essay.objects.all().filter(teacher=user.email).order_by('-created_on')
        except Essay.DoesNotExist:
            essays = []

    context = {
        'essays' : essays,
        'name' : user.get_full_name(),
        "search": query != ""
    }
    return render(request, "teacher.html", context)
    
@login_required(login_url="login")
def grade(request, pk): #max 10000 characters/request, <100 requests/day 
    context = {
        'method': request.method
    }
    essay = Essay.objects.get(pk=pk)
    user = request.user
    if user.student:
        return redirect("home")
    if request.method == 'POST' and not essay.graded:
        client = GrammarBotClient()
        edited_body = ""
        cursor = 0
        body = essay.body
        result = client.check(body)
        print(result)
        
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
        context['essay'] = reformat(edited_body)

    else:
        context['essay'] = essay.marked_body

    context['orig'] = Essay.objects.get(pk=pk)
    essay.graded = True
    essay.marked_body = context['essay']
    
    essay.save()

    return render(request, "grade.html", context)

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
    
@login_required(login_url="login")
def teacher_detail(request, pk):
    user = request.user

    if user.student:
        redirect("home")

    try:
        essay = Essay.objects.get(pk=pk)
    except Essay.DoesNotExist:
        essay = {}

    context = {
        'essay' : essay,
    }
    return render(request, "teacher_detail.html", context)
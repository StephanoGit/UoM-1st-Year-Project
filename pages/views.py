import queue
import re
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q,Avg
from .models import Region, Accommodations,Comment,Question, Image_table
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
import pandas as pd

from django.contrib import messages
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.decorators.csrf import csrf_exempt

# own views
from .forms import CreateUserForm, CommentForm, QuestionForm, AnswerForm

# external
from better_profanity import profanity


# Create your views here.

#home page
def home_view(request, *args, **kwargs):
    accom = Accommodations.objects.all()
    region = Region.objects.all()
    context = {"accom": accom , "region":region}
    return render(request , 'home.html' , context)


#loading page
def loading_view(request, *args, **kwargs):
    return render(request, 'loadingPage.html', {})


#any accommodation page
def accommodation(request , pk, *args, **kwargs):
    showbuttonComments = True
    showbuttonQuestions = True
    accom = Accommodations.objects.get(id=pk)
    images = Image_table.objects.filter(accommodation = accom.id)

    #format name for the GOOGLE API search.
    linkAccom = accom.name
    linkAccom = linkAccom.replace(' ', '%20')
    postCode = accom.post_code
    if postCode != None:
        postCode = postCode + '%20'
    else:
        postCode = 'Manchester%20University' + '%20'

    # comments checking for profanity / bad words
    comments_raw = Comment.objects.filter(accommodation_id = accom.id)
    comments_all = comments_raw
    if len(comments_raw) > 3:
        comments_raw = comments_raw[:3] 
    if request.method == "POST":
        sc = request.POST.get('comment_btnn')
        if sc == "1":
            comments_raw = comments_all  
            showbuttonComments = False  
    
    for comment in comments_raw:
        comment.comment = profanity.censor(comment.comment)
        
    questions_raw = Question.objects.filter(accommodation_id = accom.id)
    questions_all = questions_raw
    if len(questions_raw) > 3:
        questions_raw = questions_raw[:3]
    if request.method == "POST":
        sc = request.POST.get('question_btnn')
        if sc == "2":
            questions_raw = questions_all 
            showbuttonQuestions = False
            
    for question in questions_raw:
        question.question = profanity.censor(question.question)
        question.answer = profanity.censor(question.answer)

    overall = Comment.objects.filter(accommodation_id = accom.id).aggregate(Avg('overall'))
    context = {"accom": accom ,"linkAccom": linkAccom , "postCode": postCode, "comments": comments_raw, "questions": questions_raw,
    "overall": overall, "images": images, "showbuttonComments": showbuttonComments, "showbuttonQuestions": showbuttonQuestions}
    return render(request , "accommodation.html" , context)

#search/ filter page
def search(request, *args, **kwargs):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    accom = Accommodations.objects.filter(Q(name__contains = q)| Q(region__name__contains = q))
    bathroom = []
    catering = []
    price = []
    campus = []

    for image in accom:
        image.image = '/images/' + str(image.image)

    if request.method == "POST":
        filter = request.POST.getlist("filter_objects")
        for i in filter:
            if i in ["Catered" , "Self-catered"]:
                catering.append(i)
            elif i.isdigit():
                price.append(int(i))
            elif i in ["Shared" , "En Suite"]:
                bathroom.append(i)
            elif i in ["Victoria Park" , "City Centre" , "Fallowfield"]:
                campus.append(i)
            else:
                pass
    accom_data = Accommodations.objects.values("name" , "price" , "catering" , "campus" , "bathroom", "image")

    accomdf = pd.DataFrame(accom_data)
    accomdf.index = accomdf.index + 1
    if bathroom != []:
        accomdf = accomdf[accomdf["bathroom"].isin(bathroom)].dropna()
    if campus != []:
        accomdf = accomdf[accomdf["campus"].isin(campus)].dropna()
    if catering != []:
        accomdf = accomdf[accomdf["catering"].isin(catering)].dropna()
    if price != []:
        for i in price:
            if i ==  150:
                accomdf = accomdf[accomdf["price"] > 150]
            elif i == 130: 
                accomdf = accomdf[(accomdf["price"] < 150) & (accomdf["price"] > 130) ]
            elif i == 100:
                accomdf = accomdf[((accomdf["price"] < 130) & ((accomdf["price"] > 100)))]
    accom_filter = accomdf.to_dict()

    new_dict = accom_filter["name"]
    img_dict = accom_filter["image"]

    for key in img_dict.keys():
        img_dict[key] = '/images/' + str(img_dict[key])

    zip_dict = zip(new_dict.items(), img_dict.items())

    context = {"accom": accom , "accom_id" : new_dict, "zip_dict": zip_dict}
    return render(request , "search.html", context)

#comment page, login is required
@login_required(login_url='loginPage')
def comment(request):
    q = request.GET.get('addcomm_button_hidden') if request.GET.get('addcomm_button_hidden') != None else ''
    try:
        accommodation = Accommodations.objects.get(id = q)
    except:
        form = CommentForm()
    else:
        form = CommentForm(initial={'accommodation': accommodation})
    if request.method == "POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment.save(commit=False)

            value_of_money = request.POST.get('vom-rating')
            location = request.POST.get('loc-rating')
            internet = request.POST.get('int-rating')
            social = request.POST.get('soc-rating')
            overall = request.POST.get('overall-rating')

            comment.instance.value_of_money = value_of_money
            comment.instance.location = location
            comment.instance.internet = internet
            comment.instance.social = social
            comment.instance.overall = overall

            comment.save()
            accom = comment.cleaned_data.get("accommodation")
            returnid = Accommodations.objects.get(name = accom)
            return redirect('https://marss-project.herokuapp.com/accommodation'+ '/' + str(returnid.id))
    context = {"form": form}
    return render(request , 'comment.html' , context)


#question page, login is required
@login_required(login_url='loginPage')
def question(request):
    q = request.GET.get('askques_button_hidden') if request.GET.get('askques_button_hidden') != None else ''
    accommodation = Accommodations.objects.get(id = q)
    form = QuestionForm(initial={'accommodation': accommodation})
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid:
            form.save()
            accom = form.cleaned_data.get("accommodation")
            returnid = Accommodations.objects.get(name = accom)
            return redirect('https://marss-project.herokuapp.com/accommodation'+ '/' + str(returnid.id))
    context = {"form" : form}
    return render(request , 'question.html' , context)


#answer page, login is required
@login_required(login_url='loginPage')
def answer(request):
    q = request.GET.get('answer_button_hidden') if request.GET.get('answer_button_hidden') != None else ''
    question = Question.objects.filter(id = q).values()
    test = Question.objects.filter(id = q)
    answer = request.POST.get('answer')
    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid:
            ques = Question.objects.get(id=q)
            ques.answer = answer
            ques.save(update_fields=['answer'])
            accomid = question.get()["accommodation_id"]
            return redirect('https://marss-project.herokuapp.com/accommodation'+ '/' + str(accomid))
    context = {"form": form, "question" : question.get()}
    return render(request , 'answer.html' , context)


#login page
@csrf_exempt
def login_view(request, *args, **kwargs):
    form = CreateUserForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("homePage")
        else:
            messages.error(request, "Your username or password was incorrect or your account is inactive. Please check your email inbox for activation.")

    context = {"form": form}
    return render(request, "login.html", context)


#if logout, return to homepage
def logout_view(request , *args , **kwargs):
    logout(request)
    return redirect("homePage")


#about page
def about(request):
    return render(request , "about.html")

#terms and conditions page
def terms_and_conditions(request):
    return render(request , "terms_and_conditions.html")

#register page
@csrf_exempt
def register_view(request, *args, **kwargs):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid() and "manchester.ac.uk" in form.cleaned_data.get("email"):
            sendEmail(request)
            messages.success(request, "Account was created for " + form.cleaned_data.get("username"))
            return redirect("loginPage")

        #display the errors
        else:
            messages.error(request, "You provided an invalid email and/or you passwords did not match.")
            messages.error(request, "You must use your Manchester University account.")
            messages.error(request, "Your password must be at least 8 characters long and contain: numbers, symbols and upper cases")
            messages.error(request, "Check if you already have an account.")

    context = {"form": form}
    return render(request, "register.html", context)


#email verification
@csrf_exempt
def sendEmail(request):
    password = request.POST.get("password1")
    username = request.POST.get("username")
    email = request.POST.get("email")
    
    user = get_user_model().objects.create(username=username, password=make_password(password), email=email)
    user.is_active = False

    send_email(user)

    return render(request, 'confirm_email.html')

#ranking page
def about_view(request):
    return render(request, "about.html", {})

def ranking_view(request):
    data = Comment.objects.all().values('overall' , 'accommodation__name')
    data_frame = pd.DataFrame(data)
    average_score_raw = data_frame.groupby("accommodation__name").mean()
    sorted_score = average_score_raw.sort_values("overall" , ascending=False)
    final_score = sorted_score["overall"].round(1)
    final_score_dictionary = final_score.to_dict()
    context = {'dataframe' : final_score_dictionary}
    return render(request, "ranking.html", context)


#error page
def error404_view(request):
    return render(request, "error404.html", {})

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from .forms import UserRegistrationForm
from .models import chatMessages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel

import json,datetime
from django.core import serializers
# Create your views here.

fname = ''
def home(request):
    return render(request,"authentication/index.html")

@login_required(login_url='signin')
def dashboard(request):
    global fname
    routes = Journey.objects.all()
    q = request.GET.get('q')
    try:
        q = q.split('-->')
        journeys = None
        if len(q) == 2:
            journeys = Journey.objects.filter(
                Q(source__source=q[0]) &
                Q(dest__dest=q[1])
            )
        else:
            journeys = Journey.objects.filter(
                Q(source__source__icontains=q[0])
                | Q(dest__dest__icontains=q[0])
                | Q(d_date__icontains=q[0])
                | Q(pname__username__icontains=q[0])
            )
    except:
        journeys = routes
    r = []
    for i in routes:
        s = str(i.source) + '-->' + str(i.dest)
        if s not in r:
            r.append(s)
    r.sort()
    context = {'fname': User.objects.get(username=request.user), 'journey_count': len(journeys), 'routes': r, 'journeys': journeys}
    return render(request, 'authentication/dash.html', context)



def signup(request):
    if request.method == "POST":
        username= request.POST['username']
        fname = request.POST['fname']
        # lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already registered! ")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request,"Username must be under 10 charaacters")
            return redirect('home')

        if pass1!=pass2:
            messages.error(request,"Passwords didn't match!")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username Must be alpha numeric")
            return redirect('home')


        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        # myuser.last_name=lname

        myuser.save()

        messages.success(request,"Your account has been succesfully created")

        return redirect('signin')




    return render(request,"authentication/signup_hack.html")



def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        pass1= request.POST['pass1']

        user=authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname= user.first_name
            return render(request,"authentication/dash.html",{'fname':fname})
            
        else:
            messages.error(request,"Bad Credentials!")
            return redirect('home')
    return render(request,"authentication/hacktivity.html")



def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')



@login_required(login_url='signin')
def createJourn(request):
    form = JournForm()
    if request.method == 'POST':
        form = JournForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(username=request.user)
            obj.pname = user
            obj.save()
            return redirect('dash')
    context = {'fname': fname, 'form': form, 'type': 'Create'}
    return render(request, 'authentication/create_journ.html', context)



@login_required(login_url='signin')
def updateJourn(request, pk):
    route = Journey.objects.get(id=pk)
    form = JournForm(instance=route)
    if request.method == 'POST':
        form = JournForm(request.POST, instance=route)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(username=request.user)
            obj.pname = user
            obj.save()
            return redirect('dash')
    context = {'fname': fname, 'form': form,'type': 'Update'}
    return render(request, 'authentication/create_journ.html', context)



@login_required(login_url='signin')
def deleteJourn(request, pk):
    route = Journey.objects.get(id=pk)
    route.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required
def chat_home(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"chat1-home",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"authentication/home.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account successfully created!')
            return redirect('chat-login')
        context = {
            "page":"register",
            "form" : form
        }
    else:
        context = {
            "page":"register",
            "form" : UserRegistrationForm()
        }
    return render(request,"authentication/register.html",context)

@login_required
def profile(request):
    context = {
        "page":"profile",
    }
    return render(request,"authentication/profile.html",context)

def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post =request.POST
        
        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        insert = chatMessages(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")



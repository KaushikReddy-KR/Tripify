from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

fname = ''
# Create your views here.

def home(request):
    return render(request, "base/home.html", {'fname': fname})

@login_required(login_url='login')
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
    context = {'fname': User.objects.get(username=fname), 'journey_count': len(journeys), 'routes': r, 'journeys': journeys}
    return render(request, 'base/dash.html', context)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered! ")
            return redirect('dash')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 charaacters")
            return redirect('dash')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('dash')
        if not username.isalnum():
            messages.error(request, "Username Must be alpha numeric")
            return redirect('dash')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been succesfully created")

        return redirect('login')

    return render(request, "base/signUp.html")


def login_page(request):
    global fname
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname1 = user.first_name
            fname = fname1
            return redirect('dash')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('dash')
    return render(request, "base/login_page.html")


def logout_page(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('dash')

@login_required(login_url='login')
def createJourn(request):
    form = JournForm()
    if request.method == 'POST':
        form = JournForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(username='Mark')
            obj.pname = user
            obj.save()
            return redirect('dash')
    context = {'fname': fname, 'form': form, 'type': 'Create'}
    return render(request, 'base/create_journ.html', context)

@login_required(login_url='login')
def updateJourn(request, pk):
    route = Journey.objects.get(id=pk)
    form = JournForm(instance=route)
    if request.method == 'POST':
        form = JournForm(request.POST, instance=route)
        if form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.get(username='Mark')
            obj.pname = user
            obj.save()
            return redirect('dash')
    context = {'fname': fname, 'form': form,'type': 'Update'}
    return render(request, 'base/create_journ.html', context)

@login_required(login_url='login')
def deleteJourn(request, pk):
    route = Journey.objects.get(id=pk)
    route.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

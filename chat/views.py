from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
from chat.forms import CALForm
from chat.models import LOG


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = CALForm()
        logs = LOG.objects.order_by('-date')[:10]
        return render(request, 'index.html', context={'form': form, 'logs': logs})


def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form": form1
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)


def signout(request):
    logout(request)
    return redirect('login')

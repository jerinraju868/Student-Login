from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, logout, authenticate
from .forms import  RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Student


def Register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            age = form.cleaned_data['age']
            higher_studies = form.cleaned_data['higher_studies']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exist')
                return redirect('register')

            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name, email=email, username=username, password=password)
                user.set_password(password)
                user.save()

                student = Student.objects.create(student=user, age=age, higher_studies=higher_studies)
                student.save()

                return redirect('login')

        else:
            messages.error(request, 'Something went wrong.!')
            return redirect('register')

    else:
        form = RegisterForm()
        return render(request,'register.html',{'form':form})

def Login(request):

    if request.method == "POST":

        username = request.POST['username']
        password =  request.POST['password']
        
        user = authenticate(request,username=username,password=password)

        if user is not None:

            if user.is_active:
                form = login(request, user)
                return redirect('/')

            else:
                messages.error(request, 'user is disabled.! please contact admin')
                return redirect('login')

        else:
            messages.error(request, 'invalid username or password.!')
            return redirect('login')

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
        
def Home(request):

    if request.user.is_authenticated:
        return render(request, 'home.html')

    else:
        return redirect('login') 

def Logout(request):
    
    logout(request)
    return redirect('login')
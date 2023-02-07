# Student_Project

## Create virtualenvironment and setup
    python -m venv Env
    source Env/bin/activate
### install django in virtualenvironment
    pip install django

## Create Project
    django-admin startproject Student_project

## Create app
    cd Student_project
    python manage.py startapp App

# setting.py

## importing package
    import os

## Add app name in installed apps
    INSTALLED_APPS = [
        'App',
    ]

## Add Templates folder path
    os.path.join(BASE_DIR, 'templates')

then, save the setting.py

# Create a folder templates in the project parent directory and html files
![Screenshot from 2023-02-06 00-23-39](https://user-images.githubusercontent.com/117073931/216839037-d4627694-248b-4349-9938-d37866156d27.png)


# Create a model named as Stundent
## App/model.py
    from django.db import models
    from django.contrib.auth.models import User

    class Student(models.Model):
        student = models.ForeignKey(User, on_delete=models.CASCADE)
        age = models.IntegerField()
        higher_studies = models.BooleanField(default=False)

        def __str__(self):
            return self.username

# Makemigration and Migrate
    python manage.py makemigrations
    python manage.py migrate

# Creating the super user
    python manage.py createsuperuser
add the credentials for the super user

# run the server
    python manage.py runserver

# Student_Project/urls.py

## Add App.urls in the Student_Project/urls.py
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('App.urls')),
    ]
save the Student_Project/urls.py

# App

## Create a file called urls.py in App folder
### App/urls.py 
    from django.urls import path
    from App import  views

    urlpatterns = [
        path('',views.Home, name='home'),
        path('login',views.Login, name='login'),
        path('register',views.Register, name='register'),
        path('logout',  views.Logout, name='logout'),
    ]

## Create a file called forms.py in App folder
### App/forms.py
    from django import forms
    from django.contrib.auth.models import User
    from App.models import Student

    class RegisterForm(forms.ModelForm):
        first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}))
        last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}))
        email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'example@gmail.com'}))
        username = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
        password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'********'}))
        age = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Age'}))
        higher_studies = forms.BooleanField(label='Eligible for higher studies',required=False)
        
        class Meta:
            model = Student 
            fields = ['first_name','last_name','age','email','username','password','higher_studies']


    class LoginForm(forms.ModelForm):
        username = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username',}))
        password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'********'}))
        
        class Meta:
            model = User
            fields = ['username', 'password']

# App/views.py

## importing the files and packages
    from django.shortcuts import render, redirect
    from django.contrib.auth.models import auth, User
    from django.contrib.auth import login, logout, authenticate
    from .forms import  RegisterForm, LoginForm
    from django.contrib import messages
    from django.contrib.auth.hashers import make_password
    from .models import Student

## Creating the function for registration
### App/views.py
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

### templates/base.html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        {% block title %}
        <title>SMS</title>
        {% endblock title %}
    </head>
    <body style="background-color:rgb(206, 206, 206)">
        
        <nav class="navbar navbar-light bg-light">
            <div style="display: flex;">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNoVbwPTEUPvAiZemASQu7OZ3G0uAydp-2uw&usqp=CAU" alt="logo" style="width: 50px; margin-left: 50px;">&nbsp;&nbsp;
                <label >
                    <a class="navbar-brand" href="{% url 'home' %}" style="font-size: xx-large; font-weight: bolder; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                        Student Management System
                    </a>
                    </label>
            </div>
            <ul style="list-style: none; display: flex; margin-right:30px">
                {% if user.is_authenticated %}
                <li>
                    <svg xmlns="http://www.w3.org/2000/svg" style="width:25px;height:25px"  fill="currentColor" class="bi bi-unlock-fill" viewBox="0 0 16 16">
                        <path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2z"/>
                    </svg>
                    
                    <a href="{% url 'logout' %}" style="margin-right: 50px; text-decoration: none;">Logout</a>
                </li>
                {% else %}
                <li>
                    <svg xmlns="http://www.w3.org/2000/svg" style="width:25px;height:25px;color:blue"  fill="currentColor" class="bi bi-lock-fill" viewBox="0 0 16 16">
                        <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                    </svg>
                    
                    <a href="{% url 'login' %}" style="margin-right: 50px; text-decoration: none;">Login</a>
                </li>

                <li>
                    <svg xmlns="http://www.w3.org/2000/svg" style="width:25px;height:25px;color:green" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
                    </svg>
                
                    <a href="{% url 'register' %}" style=" text-decoration: none;">Register</a>
                </li>
                {% endif %}
            </ul>
        </nav>
        <br>
        {% block content %}
        {% endblock content %}
    </body>
    </html>

### templates/register.html
    {% extends 'base.html' %}
    {% block title %}
    <title>Register</title>
    {% endblock title %}

    {% block content %}
    <div class="container" style="display: flex;align-items: center;justify-content: center;">
        <div class="card shadow" style="width:40%; height:auto;border-radius: 1rem;margin-top: 60px;">
            <div class="card-title">
                <h1 align="center" style="margin-top: 25px;font-family: Arial, Helvetica, sans-serif;">Registration Page </h1>
            </div>
            <div class="card-body">
                <div class="error">
                    {% for message in messages %}
                    <p class="text-danger" style="font-style:italic">{{ message }}</p>
                    {% endfor %}
                </div>
                <form method="post">
                    {% csrf_token %}
                    {{form.as_p}}
                    <center>
                        <input type="submit" class="btn btn-success" value="Register">
                    </center><br>
                    <div class="" style="text-align: center;">
                        Already have an account.?
                        <a href="{% url 'login' %}" style="font-style: italic;">Login</a>
                    </div><br>
                </form>
            </div>
        </div>
    </div>
    {% endblock content %}
### Browser View
![Screenshot from 2023-02-07 14-29-16](https://user-images.githubusercontent.com/117073931/217198795-511b548f-dde0-426d-8f38-3143cdba382d.png)


## Creating the function for login
### App/views.py
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

### templates/login.html
    {% extends 'base.html' %}
    {% block title %}
    <title>Login</title>
    {% endblock title %}

    {% block content %}
    <div class="container" style="display: flex;align-items: center;justify-content: center;">
        <div class="card shadow" style="width:40%; height:auto;border-radius: 1rem;margin-top: 60px;">
            <div class="card-title">
                <h1 align="center" style="margin-top: 25px; font-family: Arial, Helvetica, sans-serif;">Login Page </h1>
            </div>
            <div class="card-body">
                <div class="error">
                    {% for message in messages %}
                    <p class="text-danger" style="font-style:italic">{{ message }}</p>
                    {% endfor %}
                </div>
                <form method="post">
                    {% csrf_token %}
                    {{form.as_p}}
                    <center>
                        <input type="submit" class="btn btn-primary" value="Login">
                    </center><br>
                    <div class="" style="text-align: center;">
                        Don't have an account.
                        <a href="{% url 'register' %}" style="font-style: italic;">Register</a>
                    </div><br>
                </form>
            </div>
        </div>
    </div>
    {% endblock content %}
### Browser View
![Screenshot from 2023-02-07 14-31-02](https://user-images.githubusercontent.com/117073931/217199176-4c582259-d24d-4065-8ccd-9d05be15ef80.png)


## Creating the function for home
### App/views.py
    def Home(request):
        if request.user.is_authenticated:
            return render(request, 'home.html')
        else:
            return redirect('login') 


### templates/home.html
    {% extends 'base.html' %}
    {% block title %}
    <title>Home</title>
    {% endblock title %}

    {% block content %}
    <div class="container fluid" style="display:flex;justify-content: center;color: white;">
        <div class="card shadow"  style="width:880px;height:550px;border-radius: 1rem;background-image: url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRi_pu3-xUpS6-qUHs7oXrw40FC7_IWgFViZw&usqp=CAU);background-repeat: no-repeat;background-size: contain">
            <div class="card-title">
                <h1 align="center" style="margin-top: 25px; font-family: Arial, Helvetica, sans-serif;">Home Page </label>
            </div>
            <div class="card-body" style="text-align: right;">
            <h1>Hai {{user.username}},</h1>
            <h5>Welcome to Home page.</h5>
            </div>
        </div>
    </div>
    {% endblock content %}
### Browser View
![Screenshot from 2023-02-07 14-30-31](https://user-images.githubusercontent.com/117073931/217199077-f1cf3650-51db-4797-8d6a-f54e34f81379.png)

## Creating the function for logout
### App/views.py
    def Logout(request):
        logout(request)
        return redirect('login')

# run the server
    python manage.py runserver


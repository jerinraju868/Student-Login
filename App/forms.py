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
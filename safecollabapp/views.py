from django.shortcuts import render

def login(request): # Home page and login screen
    return render(request, 'login.html')

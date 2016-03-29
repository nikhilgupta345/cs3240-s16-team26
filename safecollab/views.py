from django.shortcuts import render, redirect

def login_redirect(request): # Home page and login screen
    return redirect('login/')

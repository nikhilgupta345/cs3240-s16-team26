from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login(request): # Home page and login screen
    # Initially empty as we don't know if their password was invalid
    context_dict = {
        'login_message': ''
    }
    
    if request.method == 'POST': # Check if they submitted the login form

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) # Check if this username/password combo exists
        if user is not None:
            login(request, user) # Log the user in if they do
        else:
            context_dict['login_message'] = 'Invalid username and password combination.'

    # If on site before logging in or they had invalid credentials we send them to login page
    return render(request, 'login.html', context_dict)

def register(request):
    return None

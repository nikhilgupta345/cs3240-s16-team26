from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

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
            auth_login(request, user) # Log the user in if they do
            request.session['username'] = username
            return render(request, 'index.html')
        else:
            context_dict['login_message'] = 'Invalid username and password combination.'
    elif 'username' in request.session:
        return render(request, 'index.html')

    # If on site before logging in or they had invalid credentials we send them to login page
    return render(request, 'login.html', context_dict)

def logout(request):
    print("Test output")
    try:
        user = request.session['username']
        del request.session['username']
        print("logged out user " + user)
    except KeyError:
        print("User not found")
        pass

    print("This")
    return redirect('/', permanent=True)

def register(request):
    return None

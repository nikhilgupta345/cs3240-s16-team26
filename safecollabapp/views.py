from django.shortcuts import render

def login(request): # Home page and login screen
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)
        return render(request, 'login.html')

    else:
        return render(request, 'login.html')

from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
#from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.http import HttpResponse
from safecollabapp.models import PrivateMessage

#---------------------------------
# added for file upload example
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from safecollabapp.models import Document
from safecollabapp.forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('safecollabapp.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

#---------------------------------

# Uncomplete at the moment.
def recover_password(request):
    return render(request, 'recover_password.html');

# Returns whether a user is a site-manager or not
def is_manager(user):
    try:
        manager_group = Group.objects.get(name='site-manager')
    except:
        g = Group(name='site-manager')
        g.save()
        return False
    
    return user in manager_group.user_set.all()

# Returns a list of Users who are Site-Managers
def get_managers():
    return User.objects.filter(groups__name='site-manager')

def add_user_to_group(request):
    if request.method == "POST":
        context_dict = {
            'response': ''
        }

        group_name = request.POST.get('group_name')
        username = request.POST.get('username')

        g = Group.objects.get(name=group_name)
        try:
            print(username)
            user = User.objects.get(username=username)
            if user in g.user_set.all():
                context_dict['response'] = 'User already in group!'
            else:
                user.groups.add(g)
        except:
            context_dict['response'] = 'Invalid User!'

        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    else:
        return redirect('/index/')

def create_group(request):
    if request.method == 'POST': # Check if they submitted the form to create a new group
        name = request.POST.get('group_name') # Get the group name that they wish to add
        context_dict = {
            'response' : '',
            'usernames': [],
        }

        users = User.objects.all()
        for user in users:
            context_dict['usernames'].append(user.username)


        if len(name) == 0:
            context_dict['response'] = 'You must enter a group name.'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

        try:
            g = Group.objects.get(name=name)

            context_dict['response'] = 'There is already a group on the site with that name!'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")
        except:                
            g = Group(name=name)
            g.save()    
            request.user.groups.add(g)

        return HttpResponse(json.dumps(context_dict), content_type="application/json")

    else:
        return redirect('/index/')

def add_manager(request):
    if request.method == 'POST': # Check if they submitted the form to add an SM
        if not is_manager(request.user): # Check if they even have permission to add a new SM
            return redirect('/index/')

        username = request.POST.get('username') # Get the username that they wish to add
        context_dict = {
            'response':''
        }

        if len(get_managers()) == 3:
            context_dict['response'] = 'There are already 3 superusers -- you cannot add anymore!'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")
        try:
            new_manager = User.objects.get(username=username)
        except:
            context_dict['response'] = 'Could not find a user with that username'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")
            
        if new_manager is not None: # User exists
            if is_manager(new_manager): # Already a manager
                context_dict['response'] = 'That user is already a Site Manager!'
            else:
                manager_group = Group.objects.get(name='site-manager')
                new_manager.groups.add(manager_group)
                context_dict['response'] = 'Successfully added ' + username + ' as a Site Manager.'
        
        return HttpResponse(json.dumps(context_dict), content_type="application/json")

    else:
        return redirect('/index/')

def suspend_user(request):
    if request.method == 'POST': # Check if they submitted a request to suspend a user
        if not is_manager(request.user): # Check if they even have permission
            return redirect('/index/')

        username = request.POST.get('username') # Get the username that they wish to add
        context_dict = {
            'response':''
        }

        user = User.objects.get(username=username)

        if not user.is_active:
            context_dict['response'] = 'That user has already been suspended!'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

        else:
            user.is_active = False
            user.save()
            context_dict['response'] = 'That user has been successfully suspended.'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

    else:
        return redirect('/index/')

def restore_user(request):
    if request.method == 'POST': # Check if they submitted a request to suspend a user
        if not is_manager(request.user): # Check if they even have permission
            return redirect('/index/')

        username = request.POST.get('username') # Get the username that they wish to add
        context_dict = {
            'response':''
        }

        user = User.objects.get(username=username)

        if user.is_active:
            context_dict['response'] = 'That user is already active!'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

        else:
            user.is_active = True
            user.save()
            context_dict['response'] = 'That user has been successfully restored.'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

    else:
        return redirect('/index/')

def index(request):
    if not request.user.is_authenticated(): # If not logged in send back to login page
        return redirect('/login/')
    group_info = []
    groups = request.user.groups.exclude(name='site-manager')

    for group in groups:
        group_info.append({
            'group':group, 
            'num_users':len(group.user_set.all())
        })


    context_dict = {
        'is_manager': is_manager(request.user), # Is this user a manager?
        'site_managers_list' : get_managers(), # the list of current site-managers
        'users_list' : User.objects.all(),
        'messages' : get_messages(request.user),
        'groups' : group_info,
    }

    return render(request, 'index.html', context_dict)

def login(request): # Home page and login screen
    # Initially empty as we don't know if their password was invalid
    context_dict = {
        'login_message': '',
        'register_message': '',
    }

    if request.method == 'POST': # Check if they submitted the login form

        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember') # Remember me checkbox

        user = authenticate(username=username, password=password) # Check if this username/password combo exists
        if user is not None:
            if not user.is_active:
                context_dict['login_message'] = 'Your account has been suspended. Please contact a site-manager.'
                return render(request, 'login.html', context_dict)

            auth_login(request, user) # Log the user in if they do
            if(remember is not None):
                request.session['username'] = username # Set a session so they're remembered next time

            return redirect('/index/')
        else:
            context_dict['login_message'] = 'Invalid username and password combination.'
    elif 'username' in request.session:
        return redirect('/index/')

    # If on site before logging in or they had invalid credentials we send them to login page
    return render(request, 'login.html', context_dict)

def logout(request):
    auth_logout(request)
    return redirect('/', permanent=True) # Redirect to front page

def register(request):
    # Initially empty -- will be set later
    context_dict = {
        'login_message': '', # Message for the login page about authentication being unsuccessful
        'register_message': '', # Message for the register page about errors in the form
        'response': '', # Response = fail or success for JS later on
    }
    if request.method == 'POST':
        # Retrieve POST data
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Validate this data

        # Make sure that all fields are filled out
        if first_name == '' or last_name == '' or username == '' or email == '' or password == '' or confirm_password == '':
            context_dict['register_message'] = 'You must fill out all fields to register.'
            context_dict['response'] = 'fail'
        # Make sure that username is alphanumeric
        elif username.isalnum() == False:
            context_dict['register_message'] = 'Your username can only contain numbers and letters.'
            context_dict['response'] = 'fail'
        # Minimum length of 8 on passwords
        elif len(password) < 8:
            context_dict['register_message'] = 'Your password must have at least 8 characters.'
            context_dict['response'] = 'fail'
        elif password != confirm_password: # Passwords differ
            context_dict['register_message'] = 'The two passwords do not match.'
            context_dict['response'] = 'fail'
        else:
            try: # Need to check if this email is valid
                validate_email(email)

                # Does this user already exist? Either email or username can't be duplicated.
                user_by_username = User.objects.filter(username=username)
                user_by_email = User.objects.filter(email=email)

                if len(user_by_username) != 0:
                    context_dict['register_message'] = 'That username is already in use.'
                    context_dict['response'] = 'fail'
                elif len(user_by_email) != 0:
                    context_dict['register_message'] = 'That email is already in use.'
                    context_dict['response'] = 'fail'
                else:
                    # Create this new user with these parameters
                    user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        email = email,
                        username = username,
                        password = password
                    )

                    user.save()

                    user = authenticate(username = username, password = password) # Authenticate him with these credentials
                    if user == None:
                        context_dict['response'] = 'redirect_login'
                        return HttpResponse(json.dumps(context_dict), content_type="application/json")

                    auth_login(request, user) # Log the user in if they do
                    
                    request.session['username'] = username # Set a session so they're remembered next time

                    if username == "admin": # Username 'admin' is a default site-manager if not already full
                        try:
                            g = Group.objects.get(name='site-manager')
                        except:
                            g = Group(name='site-manager')
                            g.save()
                            pass

                        num_managers = len(g.user_set.all())
                        if num_managers is not 3: # Already full
                            user.groups.add(g)

                    context_dict['response'] = 'redirect_index'
                    return HttpResponse(json.dumps(context_dict), content_type="application/json")
            except ValidationError:
                context_dict['register_message'] = 'That is not a valid email address.'
                context_dict['response'] = 'fail'
                pass


        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    else: # request method not POST
        return redirect('/', permanent=True)

def messages(request):
    return redirect('/index/')

def send_message(request):
    if request.method == 'POST':
        sender = request.user
        recipient = User.objects.filter(username = request.POST.get('recipient'))[0]
        message = request.POST.get('message')

        new_msg = PrivateMessage(sender = sender, recipient = recipient, text = message)
        new_msg.save()

    return redirect('/index/')

# gets all messages sent to a certain user
def get_messages(user):
    return PrivateMessage.objects.filter(recipient=user)

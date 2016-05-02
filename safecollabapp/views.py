from django.db.models.functions import Lower
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
#from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json
from django.http import HttpResponse
from safecollabapp.models import PrivateMessage, Folder, Report, RFile
from Crypto.Hash import SHA256
from Crypto.Cipher import AES, blockalgo

#---------------------------------
# added for file upload example
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from safecollabapp.models import Document
from safecollabapp.forms import DocumentForm, SearchReportsForm

#------------------------------------
# added for search
from django.db.models import Q
from functools import reduce
import operator

from safecollabapp.forms import DocumentForm
from rest_framework.views import APIView
from rest_framework import generics
from safecollabapp.serializers import RFile_Serializer, Report_Serializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


# search report models within data base
def search_reports(request):

    if request.method == 'POST':

        context_dict = {
            'search_results' : [],
        }

        form = SearchReportsForm(request.POST)
        if form.is_valid():

            user_input = {
                'all'           :   '',
                'short_desc'    :   '',
                'long_desc'     :   '',
                'owner'         :   '',
            }

            # parse search critieria from user input
            delimiter = ";"
            for field in user_input.keys():
                post_id = 'search-reports-' + field       # need to double check ig this is name or ID from index.html...
                user_input[field] = request.POST.get(post_id)
                user_input[field] = user_input[field].split(delimiter)

            Q_objects = {
                'all'           :   Q(),
                'short_desc'    :   Q(),
                'long_desc'     :   Q(),
                'owner'         :   Q(),
            }

            # compute Q object for 'all'
            # will use other Q object fields to store intermediates

            for item in user_input['all']:
                Q_objects['short_desc'] |= Q(short_desc__icontains=item)
                Q_objects['long_desc'] |= Q(long_desc__icontains=item)
                Q_objects['owner'] |= Q(owner__username__icontains=item)

            for field in Q_objects.keys():
                if( field != 'all'):
                    Q_objects['all'] |= Q_objects[field]

            # compute Q objects for other fields
            # reset intermediates formed in 'all' computation
            for field in Q_objects.keys():
                if( field != 'all'):
                    Q_objects[field] = Q()

            # compute Q object for other fields
            for item in user_input['short_desc']:
                Q_objects['short_desc'] |= Q(short_desc__icontains=item)

            for item in user_input['long_desc']:
                Q_objects['long_desc'] |= Q(long_desc__icontains=item)

            for item in user_input['owner']:
                Q_objects['owner'] |= Q(owner__username__icontains=item)

            # get search results
            search_results = None
            # select all Reports where name or description contains keyword
            search_results = Report.objects.filter(
                            Q_objects['all']
                            & Q_objects['short_desc']
                            & Q_objects['long_desc']
                            & Q_objects['owner']
                            ).order_by(Lower('short_desc').asc())

            """
            # Render index page with the search results and the form
            return render_to_response(
                'index.html',
                {'search_results': search_results, 'form': form},
                context_instance=RequestContext(request)
            )

            """
            # fill context_dict with fields from search_results to be displayed

            # check if user is site-manager
            username = request.user.username
            site_managers = User.objects.filter(groups__name='site-manager')
            is_site_manager = False
            for manager in site_managers:
                if(username == manager.username):
                    is_site_manager = True

            # get number of results
            num_results = request.POST['search-reports-num_results']
            print(num_results)
            show_all = True
            if(num_results != ''):
                show_all = False
                num_results = int(num_results)
            else:
                num_results = 0

            print(num_results)

            # populate search results to pass back to javascript
            result_data = []
            i = 0
            for result in search_results:
                if( (i >= num_results) and (show_all == False) ):
                    break

                if(is_site_manager == False):
                    # check if report is private and user is not owner
                    if( result.private and (result.owner.username != request.user.username)):
                        # check if private report has been assigned to any groups
                        if result.group == '' or result.group == 'Public':
                            continue
                        # get group associated with report
                        g = Group.objects.get(name=result.group)
                        # check if user is in group
                        print(g.user_set.all())
                        if request.user in g.user_set.all():
                            # if user is in group append report to result_data
                            access = "Public"
                            if result.private:
                                access = 'Private'
                            result_data.append([result.short_desc, result.long_desc, result.owner.username, access])
                            i += 1
                    else: # report is public or user is the owner
                        access = "Public"
                        if result.private:
                            access = 'Private'
                        # append report to result_data
                        result_data.append([result.short_desc, result.long_desc, result.owner.username, access])
                        i += 1
                else: # user is site_manager
                    access = "Public"
                    if result.private:
                        access = 'Private'
                    # append report to result_data
                    result_data.append([result.short_desc, result.long_desc, result.owner.username, access])
                    i += 1


            context_dict['search_results'] = result_data

            return HttpResponse(json.dumps(context_dict), content_type="application/json")


    else:
        # stay on current page
        return redirect('/index/')


def parse_search_criteria(user_input):
    criteria = []
    criteria = user_input.split(";")
    return criteria

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

def remove_user_from_group(request):
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
            if user not in g.user_set.all():
                context_dict['response'] = 'User not in group!'
            else:
                user.groups.remove(g)
        except:
            context_dict['response'] = 'Invalid User!'

        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    else:
        return redirect('/index/')

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
        elif ' ' in name:
            context_dict['response'] = 'You cannot have spaces in your group name.'
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

def sm_create_group(request):
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
        elif ' ' in name:
            context_dict['response'] = 'You cannot have spaces in your group name.'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")

        try:
            g = Group.objects.get(name=name)

            context_dict['response'] = 'There is already a group on the site with that name!'
            return HttpResponse(json.dumps(context_dict), content_type="application/json")
        except:                
            g = Group(name=name)
            g.save()    

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

    all_group_info = []
    all_groups = Group.objects.exclude(name='site-manager')

    for group in all_groups:
        all_group_info.append({
            'group':group,
            'num_users':len(group.user_set.all())
        })

    context_dict = {
        'is_manager': is_manager(request.user), # Is this user a manager?
        'site_managers_list' : get_managers(), # the list of current site-managers
        'users_list' : User.objects.all(),
        'folders_list' : get_folders(request.user),
        'files_list' : get_files(request.user),
        'reports_list' : get_reports(request.user),
        'all_reports': Report.objects.all(),
        'groups' : group_info,
        'all_groups' : all_group_info,
        'doc_form' : DocumentForm(),
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
        if request.POST.get('encrypted') == 'true':
            temp = SHA256.new(b'encrypted').digest()
            aes = AES.new(temp[:16], mode=blockalgo.MODE_CFB, IV=temp[16:32], segment_size=8)
            message = aes.encrypt(message.encode())
            new_msg = PrivateMessage(sender = sender, recipient = recipient, text = 'encrypted', encrypted = True, cipher = message)
            new_msg.save()
        else:
            new_msg = PrivateMessage(sender = sender, recipient = recipient, text = message, encrypted = False, cipher = b'')
            new_msg.save()
        return HttpResponse(json.dumps({}), content_type="application/json")

    return redirect('/index/')

# gets all messages sent to a certain user
def get_messages(request):
    if request.method == 'POST':
        sender = request.user
        recipient = User.objects.filter(username = request.POST.get('recipient'))[0]
        messages = sorted(
                (list(PrivateMessage.objects.filter(sender = recipient, recipient = request.user)) + (list(PrivateMessage.objects.filter(sender = request.user, recipient = recipient)) if sender != recipient else [])),
                key=lambda msg: msg.time)
        response = {'messages' : []}
        for message in messages:
            response['messages'].append({
                'sender' : message.sender.username,
                'time' : message.time.strftime('%a %B %d, %I:%M:%S %p %Z'),
                'text' : message.text,
                })
        return HttpResponse(json.dumps(response), content_type="application/json")

    return redirect('/index/')

# gets all messages sent to a certain user
def get_messages_decrypt(request):
    if request.method == 'POST':
        sender = request.user
        recipient = User.objects.filter(username = request.POST.get('recipient'))[0]
        messages = sorted(
                (list(PrivateMessage.objects.filter(sender = recipient, recipient = request.user)) + (list(PrivateMessage.objects.filter(sender = request.user, recipient = recipient)) if sender != recipient else [])),
                key=lambda msg: msg.time)
        response = {'messages' : []}
        for message in messages:
            if message.encrypted:
                temp = SHA256.new(b'encrypted').digest()
                aes = AES.new(temp[:16], mode=blockalgo.MODE_CFB, IV=temp[16:32], segment_size=8)
                text = aes.decrypt(bytes(message.cipher)).decode("utf-8")
                response['messages'].append({
                    'sender' : message.sender.username,
                    'time' : message.time.strftime('%a %B %d, %I:%M:%S %p %Z'),
                    'text' : text,
                    })
            else:
                response['messages'].append({
                    'sender' : message.sender.username,
                    'time' : message.time.strftime('%a %B %d, %I:%M:%S %p %Z'),
                    'text' : message.text,
                    })
        return HttpResponse(json.dumps(response), content_type="application/json")

    return redirect('/index/')

def create_report(request):
    if request.method == 'POST':
        # get all values from request
        owner = request.user
        short_desc = request.POST.get('short_desc')
        long_desc = request.POST.get('long_desc')
        private = request.POST.get('private') is not None # is the box checked?
        group = request.POST.get('group')
        file_name = request.POST.get('fname')
        encrypted = request.POST.get('encrypted') is not None # is the box checked?
        file_form = DocumentForm(request.POST, request.FILES)

        new_report = Report(owner = owner, short_desc = short_desc, long_desc = long_desc, private = private, group = group)

        # Get folder if applicable
        folder_name = request.POST.get('folder')
        if folder_name != '':
            folder = Folder.objects.filter(owner=owner, name=folder_name)[0]
            new_report.folder_id = folder

        # save new report
        new_report.save()

        if('docfile' in request.FILES):
            # create RFile for uploaded file and point to report
            new_rfile = RFile(name=file_name, owner=owner, report=new_report, docfile=request.FILES['docfile'], encrypted=encrypted)
            new_rfile.save()

    return redirect('/index/')

def get_reports(user):
    reports = []
    for report in Report.objects.all():
        if report.owner == user and report.folder_id != None:
            continue
            
        if report.owner == user: # Show a report to the owner of it
            reports.append(report)
        elif report.group == '' or report.group == 'Public':
            continue
        else:
            group = Group.objects.get(name=report.group)
            if group in user.groups.all():
                print('Name: ' + group.name)
                print(user.groups.all())
                reports.append(report)

    return reports

def get_folders(user):
    return Folder.objects.filter(owner=user)

def get_files(user):
    files = []
    for file in RFile.objects.all():
        if file.encrypted == True:
            continue

        report = file.report

        if file.owner == user:
            files.append(file)
        elif report.group == '' or report.group == 'Public':
            continue
        else:
            group = Group.objects.get(name=report.group)
            if group in user.groups.all():
                files.append(file)

    return files

def view_report(request):
    if request.method == 'POST':
        context_dict = {'short_desc' : ''}
        report = Report.objects.filter(short_desc = request.POST.get('short_desc'))[0]
        context_dict['short_desc'] = report.short_desc
        context_dict['long_desc'] = report.long_desc
        context_dict['time'] = report.time.strftime('%a %B %d, %I:%M:%S %p %Z')
        context_dict['owner'] = report.owner.username
        context_dict['is_owner'] = (report.owner == request.user)
        context_dict['file_name'] = 'No files associated with report.'
        context_dict['file_id'] = '-1'
        files = RFile.objects.filter(report=report)
        for file in files:
            context_dict['file_name'] = file.name
            if not file.encrypted:
                context_dict['file_id'] = str(file.id)
        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    return redirect('/index/')

def delete_report(request):
    if request.method == 'POST':
        reports = Report.objects.filter(owner=request.user, short_desc = request.POST.get('report_name')).delete()

        return redirect('/index/')
    return redirect('/index/')

def view_file(request):
    if request.method == 'POST':
        context_dict = {'file_name' : '', 'report_name' : ''}
        rfile = RFile.objects.filter(name = request.POST.get('file_name'))[0]
        context_dict['file_name'] = rfile.name
        context_dict['report_name'] = rfile.report.short_desc
        context_dict['file_id'] = rfile.id
        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    return redirect('/index/')

def delete_file(request):
    if request.method == 'POST':
        files = RFile.objects.filter(owner=request.user, name = request.POST.get('file_name')).delete()

        return redirect('/index/')
    return redirect('/index/')

def edit_report(request):
    if request.method == 'POST':
        report = Report.objects.filter(short_desc = request.POST.get('original_name'))[0]
        report.short_desc = request.POST.get('short_desc')
        report.long_desc = request.POST.get('long_desc')
        report.save()
    return redirect('/index/')

def create_folder(request):
    return HttpResponse(json.dumps({}), content_type="application/json")

def submit_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        folder = Folder(name=folder_name, owner=request.user)
        folder.save()
    return redirect('/index/')

def open_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        folder = Folder.objects.filter(owner=request.user, name=folder_name)[0]
        reports = Report.objects.filter(owner=request.user, folder_id=folder)

        context_dict = {'reports' : []}
        for report in reports:
            context_dict['reports'].append({'short_desc': report.short_desc, 'private' : report.private})

        return HttpResponse(json.dumps(context_dict), content_type="application/json")

    return redirect('/index/')

def edit_folder(request):
    if request.method == 'POST':
        folder = Folder.objects.filter(name = request.POST.get('original_name'))[0]
        folder.name = request.POST.get('new_name')
        folder.save()
    return redirect('/index/')

def delete_folder(request):
    if request.method == 'POST':
        folders = Folder.objects.filter(owner=request.user, name = request.POST.get('folder_name'))
        for folder in folders:
            reports = Report.objects.filter(owner=request.user, folder_id=folder)
            for report in reports:
                report.folder_id = None
                report.save()
        folders.delete()

        return redirect('/index/')
    return redirect('/index/')

def sm_delete_report(request):
    if request.method == 'POST':
        context_dict = {'response' : ''}
        report = Report.objects.filter(short_desc = request.POST.get('short_desc'))[0]
        report.delete()
        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    return redirect('/index/')

def close_folder(request):
    return HttpResponse(json.dumps({}), content_type="application/json")

def download_file(request, fid):
    file = RFile.objects.get(pk=fid)
    fname = file.docfile.name
    response = HttpResponse(file.docfile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    return response

@csrf_exempt
def standalone_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                request.session['username'] = username
                return HttpResponse(content='True')
        else:
            return HttpResponse(content='False')

#@permission_classes(isAuthenticated)
class standalone_report_list(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        reports = Report.objects.all()
        member = False
        queryset1 = []
        for report in reports:
            group = None
            if report.private and report.owner.username != username:
                if report.group == "" or report.group == "Public":
                    continue
                g = Group.objects.get(name=report.group)
                if user in g.user_set.all():
                    queryset1.append(report)
            else:
                queryset1.append(report)
        serializer = Report_Serializer(queryset1, many=True)
        return Response(serializer.data)


#@permission_classes(isAuthenticated)
class standalone_file_list(generics.ListAPIView):
    serializer_class = RFile_Serializer
    queryset = RFile.objects.all()


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='Login'), # Login page
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^add_manager/$', views.add_manager, name='Add Manager'),
    url(r'^suspend_user/$', views.suspend_user, name='Suspend a User'),
    url(r'^restore_user/$', views.restore_user, name='Restore a User'),
    url(r'^create_group/$', views.create_group, name='Create a Group'),
    url(r'^add_user_to_group/$', views.add_user_to_group, name='Add a User to a Group'),
    url(r'^index/$', views.index, name='index'),
    url(r'^recover_password/$', views.recover_password, name='Recover Password'),
    url(r'^messages/$', views.messages, name='Private Messages'),
    url(r'^sendmessage/$', views.send_message, name='Send Message'),
    url(r'^list/$', views.list, name='list'),
    url(r'^create_report/$', views.create_report, name='Create Report'),
    url(r'^view_report/$', views.view_report, name='View Report'),
    url(r'^download/(?P<fid>\d+)$', views.download_file, name='Download File'),
    url(r'^standalone_report_list/(?P<username>\w+)$', views.standalone_report_list.as_view(), name='Standalone Report List'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='Login'), # Login page
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^add_manager/$', views.add_manager, name='Add Manager'),
    url(r'^index/$', views.index, name='index'),
    url(r'^recover_password/$', views.recover_password, name='Recover Password'),
    url(r'^messages/$', views.messages, name='Private Messages'),
    url(r'^sendmessage/$', views.send_message, name='Send Message'),
    url(r'^list/$', views.list, name='list'),
]

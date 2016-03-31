from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='Login'), # Login page
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='Logout')
]

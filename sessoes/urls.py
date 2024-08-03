from django.urls import path
from . import views

urlpatterns=[
    path('',views.sessions,name='sessions'),
    path('newSession', views.newSession, name='newSession'),
]
from django.urls import path
from . import views

urlpatterns=[
    path('',views.sessions,name='sessions'),
    path('newSession', views.newSession, name='newSession'),
    path('deleteSession/<int:sessionId>', views.deleteSession, name='deleteSession'),
]
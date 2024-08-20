from django.urls import path
from . import views

urlpatterns = [
    path('', views.sessions, name='sessions'),
    path('new-session/step1/', views.newSessionStep1, name='new_session_step1'),
    path('new-session/step2/', views.newSessionStep2, name='new_session_step2'),
    path('deleteSession/<int:sessionId>/', views.deleteSession, name='deleteSession'),
    path('edit-session/step1/<int:sessionId>/', views.editSession, name='edit_session_step1'),
    path('edit-session/step2/<int:sessionId>/', views.editSessionStep2, name='edit_session_step2'),
]
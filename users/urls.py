from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns=[
    path('login/', authViews.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/',views.register, name='register'),
]
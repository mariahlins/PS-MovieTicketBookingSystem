from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns=[
    path('login/', authViews.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/',views.register, name='register'),
    path('registerStaff/',views.registerStaff, name='registerStaff'),
    path('perfil/',views.perfilClient, name='perfilClient'),
    path('perfilStaff/',views.perfilStaff, name='perfilStaff'),
    path('perfilAdmin/',views.perfilAdmin, name='perfilAdmin'),
    path('edit/',views.editProfile, name='editProfile'),
    path('editStaff/<int:userId>',views.editStaff, name='editStaff'),
    path('recharge/',views.recharge, name='recharge'),
    path('walletDetail/',views.walletDetail, name='walletDetail'),
    path('addCreditCard/',views.addCreditCard, name='addCreditCard'),
    path('addDebitCard/',views.addDebitCard, name='addDebitCard'),
    path('user/',views.user, name='user'),
]
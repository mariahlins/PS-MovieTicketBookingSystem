from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cinemas.urls')),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
    path('sessoes/', include('sessoes.urls')),
    path('tickets/', include('tickets.urls')),
]

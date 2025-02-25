from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('evaluar/', views.evaluar_manual, name='evaluar_manual'),
    path('juzgar/<str:username>/', views.juzgar, name='juzgar'),
]

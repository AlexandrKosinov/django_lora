from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:dev_name>/', views.dev, name='dev'),
]
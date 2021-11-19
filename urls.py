from django.urls import path

from . import views

urlpatterns = [
    path('example1', views.example1, name='example1'),
    path('example2', views.example2, name='example2'),
    path('example3', views.example3, name='example3'),
    path('stores', views.example4)
]
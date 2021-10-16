from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('controller1/', views.controller_update, name='controller_update'),
    path('<str:room_name>/', views.room, name='room'),
]
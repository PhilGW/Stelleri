from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('controller1/', views.configure_controller, name='configure_controller'),
    path('configure/', views.configure_controller, name='configure_controller'),
    path('<str:room_name>/', views.room, name='room'),
]
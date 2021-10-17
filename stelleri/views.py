from django.shortcuts import render, redirect

def index(request):
    return render(request, 'stelleri/index.html')

def room(request, room_name):
    return render(request, 'stelleri/room.html', {
        'room_name': room_name
    })

def configure_controller(request):
    return render(request, 'stelleri/configure.html')
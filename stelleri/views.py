from django.shortcuts import render, redirect

def index(request):
    return render(request, 'stelleri/index.html')

def room(request, room_name):
    return render(request, 'stelleri/room.html', {
        'room_name': room_name
    })

def controller_update(request):
    return render(request, 'stelleri/controller_update.html')
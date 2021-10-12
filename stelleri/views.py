from django.shortcuts import render

def index(request):
    return render(request, 'stelleri/index.html')

def room(request, room_name):
    return render(request, 'stelleri/room.html', {
        'room_name': room_name
    })


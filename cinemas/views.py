from django.shortcuts import render
from .models import Cinema, Room
from .forms import CinemaForm, RoomForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'cinemas/index.html')

@login_required
def cinemas(request):
    cinemas=Cinema.objects.order_by('dateAdded')
    context={'cinemas':cinemas}
    return render(request, 'cinemas/cinemas.html', context)

@login_required
def cinema(request, cinemaId):
    cinema = Cinema.objects.get(id=cinemaId)
    rooms = cinema.room_set.order_by('dateAdded')
    context = {'cinema': cinema, 'rooms': rooms, 'cinemaId': cinemaId}
    return render(request, 'cinemas/cinema.html', context)

@login_required
def newCinema(request):
    if request.method!='POST':
        form=CinemaForm()
    else:
        form=CinemaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cinemas'))

    context={'form':form}
    return render(request, 'cinemas/newCinema.html', context)

@login_required
def newRoom(request, cinemaId):
    cinema = Cinema.objects.get(id=cinemaId)

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            newRoom = form.save(commit=False)
            newRoom.cinema = cinema
            newRoom.save()
            return HttpResponseRedirect(reverse('cinema', args=[cinemaId]))
    else:
        form = RoomForm()
    
    context = {'cinema': cinema, 'form': form, 'cinemaId': cinemaId}
    return render(request, 'cinemas/newRoom.html', context)

@login_required
def editCinema(request, cinemaId):
    cinema=Cinema.objects.get(id=cinemaId)

    if request.method=='POST':
        form=CinemaForm(instance=cinema, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cinemas'))
    else:
        form=CinemaForm(instance=cinema)
    
    context={'cinema':cinema, 'form': form}
    return render(request, 'cinemas/editCinema.html', context)

@login_required
def editRoom(request, roomId):
    room=Room.objects.get(id=roomId)
    cinema= room.cinema

    if request.method=='POST':
        form=RoomForm(instance=room, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cinema', args=[cinema.id]))
    else:
        form=RoomForm(instance=room)
    
    context={'room':room, 'cinema':cinema, 'form': form}
    return render(request, 'cinemas/editRoom.html', context)
from django.shortcuts import render
from .models import Movie
from .forms import MovieForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def movies(request):
    movies=Movie.objects.order_by('title')
    context={'movies':movies}
    return render(request, 'movies/movies.html', context)

def movie(request, movieId):
    movie=Movie.objects.get(id=movieId)
    context = {'movie': movie, 'movieId': movieId}
    return render(request, 'movies/movie.html', context)

def newmovie(request):
    if request.method!='POST':
        form=MovieForm()
    else:
        form=MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('movies'))

    context={'form':form}
    return render(request, 'movies/newmovie.html', context)
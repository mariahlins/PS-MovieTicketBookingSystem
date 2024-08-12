from django.shortcuts import render
from .models import Movie
from .forms import MovieForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def movies(request):
    movies=Movie.objects.order_by('title')
    context={'movies':movies}
    return render(request, 'movies/movies.html', context)

def movie(request, movieId):
    try:
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    context = {'movie': movie, 'movieId': movieId}
    return render(request, 'movies/movie.html', context)

@login_required
def newmovie(request):
    if request.method!='POST':
        form=MovieForm()
    else:
        form=MovieForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('movies'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar o formulário. Dados duplicados ou violação de integridade.")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")

    context={'form':form}
    return render(request, 'movies/newmovie.html', context)

@login_required
def deleteMovie(request, movieId):
    try:
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")

    if request.method == 'POST':
        movie.delete()
        return HttpResponseRedirect(reverse('movies'))

    context = {'movie': movie}
    return render(request, 'movies/deleteMovie.html', context)

def editMovie(request, movieId):
    try:
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    if request.method=='POST':
        form=MovieForm(instance=movie, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('movies'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form=MovieForm(instance=movie)

    context={'movie':movie, 'form':form}
    return render(request,'movie/editMovie.html', context)
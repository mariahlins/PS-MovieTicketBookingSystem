from django.shortcuts import render
from .models import Movie
from tickets.models import Ticket
from users.models import Review, Profile
from .forms import MovieForm, ReviewForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def movies(request):
    movies=Movie.objects.order_by('title')
    context={'movies':movies}
    return render(request, 'movies/movies.html', context)

def movie(request, movieId):
    try:
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    reviews=Review.objects.filter(movie=movie)

    context = {'movie': movie, 'movieId': movieId, 'reviews':reviews}
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

@login_required
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

@login_required
def newReview(request, ticketId):
    try:
        ticket=Ticket.objects.get(id=ticketId)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    movie=ticket.session.movie
    profile=request.user.profile
    
    if request.method=='POST':
        form=ReviewForm(request.POST, movie=movie, profile=profile)
        if form.is_valid():
            try:
                form.save()   
                return HttpResponseRedirect(reverse('perfilClient'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar o formulário. Dados duplicados ou violação de integridade.")
            except Exception as e:
                form.add_error(None, f"Erro inesperado: {e}")
        else:
            form.add_error(None, "Erro de validação do formulário")
    else:
        form=ReviewForm(movie=movie, profile=profile)

    context={'form':form, 'movie': movie, 'ticket':ticket}
    return render(request,'movies/newReview.html', context)

@login_required
def editReview(request, reviewId):
    try:
        review=Review.objects.get(id=reviewId)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review não encontrado")
    
    profile=request.user.profile
    movie=review.movie
    
    if request.method=='POST':
        form=ReviewForm(instance=review, data=request.POST, movie=movie, profile=profile)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('perfilClient'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form=ReviewForm(instance=review)

    context={'review':review, 'form':form}
    return render(request,'movies/editReview.html', context)

@login_required
def deleteReview(request, reviewId):
    try:
        review=Review.objects.get(id=reviewId)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review não encontrado")

    if request.method == 'POST':
        review.delete()
        return HttpResponseRedirect(reverse('perfilClient'))

    context = {'review': review}
    return render(request, 'movies/deleteReview.html', context)

def notifyNewMovie(movie):
    users=Profile.objects.filter(receive_movie_notifications=True)

    for user in users:
        context={'user':user, 'movie': movie}
        htmlContent=render_to_string('movies/newMovieNotify.html', context)
        textContent=strip_tags(htmlContent)

        email=EmailMessage(
            subject=f"Novo filme disponível: {movie.title}",
            body=textContent,
            from_email='cinepass.p3@gmail.com',
            to=[user.user.email]
        )
        email.content_subtype='html'
        email.send()
        
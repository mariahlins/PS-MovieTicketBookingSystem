from observer import Subject
from django.shortcuts import render
from observer.notifications import NewMovieNotificationObserver
from movies.models import Movie
from movies.forms import MovieForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

class MovieSystem(Subject):
    def __init__(self):
        super().__init__()
        self.add_observer(NewMovieNotificationObserver())

    def add_movie(self, request):
        if request.method != 'POST':
            form = MovieForm()
        else:
            form = MovieForm(request.POST)
            if form.is_valid():
                try:
                    movie = form.save()  # Salva o filme e guarda a instância
                    # Notifica observadores sobre o novo filme
                    movie_data = {'movie': movie}
                    self.notify_observers('new_movie', movie_data)
                    return HttpResponseRedirect(reverse('movies'))
                except IntegrityError:
                    form.add_error(None, "Erro ao salvar o formulário. Dados duplicados ou violação de integridade.")
                except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")

        context = {'form': form}
        return render(request, 'movies/newmovie.html', context)

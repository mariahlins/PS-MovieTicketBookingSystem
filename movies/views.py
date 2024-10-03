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

#listar todos os filmes cadastrados
def movies(request):
    movies=Movie.objects.order_by('title')
    context={'movies':movies}
    return render(request, 'movies/movies.html', context)

#resgatar apenas um filmes especifico passado no request
def movie(request, movieId):
    try:
        #puxa o filme pelo id passado
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    #vai filtrar todos os reviews que estão associados a esse filme para serem listados na tela
    reviews=Review.objects.filter(movie=movie)

    context = {'movie': movie, 'movieId': movieId, 'reviews':reviews}
    return render(request, 'movies/movie.html', context)

@login_required
def newmovie(request):
    if request.method!='POST':
        form=MovieForm()
    else:
        #se o metodo for post, executa as seguintes linhas
        form=MovieForm(request.POST)
        #verifica se o form é valido (ex.: verifica se não tem nenhum campo em branco)
        if form.is_valid():
            try:
                #tenta salvar as informações
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
        #busca o filme com o Id correspondente ao passado no request
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")

    if request.method == 'POST':
        #delete o filme que foi escolhido e redireciona para a página de todos os filmes
        movie.delete()
        return HttpResponseRedirect(reverse('movies'))

    context = {'movie': movie}
    return render(request, 'movies/deleteMovie.html', context)

@login_required
def editMovie(request, movieId):
    try:
        #busca o filme passado no request pelo id
        movie=Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    if request.method=='POST':
        #se o metodo for post, vai recuperar as informações atuais (informações alteradas e as não alteradas)
        form=MovieForm(instance=movie, data=request.POST)
        if form.is_valid():
            try:
                #tenta salvar as informações e redireciona para a tela de filmes
                form.save()
                return HttpResponseRedirect(reverse('movies'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        #caso contrário só completa com as informações do filme em questão
        form=MovieForm(instance=movie)

    context={'movie':movie, 'form':form}
    return render(request,'movie/editMovie.html', context)

@login_required
def newReview(request, ticketId):
    try:
        #busca o ticket que é passado no request
        ticket=Ticket.objects.get(id=ticketId)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Filme não encontrado")
    
    #resgata as informações do filme e do perfil que estão associados ao ticket
    movie=ticket.session.movie
    #request.user.profile porque profile foi uma classe criada em users/models
    profile=request.user.profile
    
    if request.method=='POST':
        #se o metodo for post vai pegar as informações que o usuário digitou e vai automaticamente completar os campos de profile e de movie
        #poderia ser form=ReviewForm(request.POST, movie=ticket.session.movie, profile=request.user.profile)
        form=ReviewForm(request.POST, movie=movie, profile=profile)
        if form.is_valid():
            #se o form não tiver nenhum problema, vai salvar as informações do review e redirecionar para a pagina de perfil do usuario
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
        #resgata o review passado no request
        review=Review.objects.get(id=reviewId)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review não encontrado")
    
    #resgata as informações do profile associado e do filme
    profile=request.user.profile
    movie=review.movie
    
    if request.method=='POST':
        #se o metodo for post, "salva o estado atual" do form e mantem o filme e o usuário
        form=ReviewForm(instance=review, data=request.POST, movie=movie, profile=profile)
        if form.is_valid():
            #se o form for válido e nao tiver problemas, salva e redireciona de volta para o perfil do cliente em questao
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
        #resgata o review passsado pelo id
        review=Review.objects.get(id=reviewId)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review não encontrado")

    if request.method == 'POST':
        #deleta usando o metodo do sql e redireciona para a pagina de perfil do cliente
        review.delete()
        return HttpResponseRedirect(reverse('perfilClient'))

    context = {'review': review}
    return render(request, 'movies/deleteReview.html', context)

def notifyNewMovie(movie):
    #busca todos os usuários que estao com campo de receber notificaçoes ativado
    users=Profile.objects.filter(receive_movie_notifications=True)

    for user in users:
        #percorre todos os usuários filtrados e passa no context o user em questao e o filme adicionado 
        context={'user':user, 'movie': movie}
        #renderiza o template HTML 'newMovieNotify.html' usando o context
        #isso converte o template em uma string com o conteúdo HTML
        htmlContent=render_to_string('movies/newMovieNotify.html', context)
        
        #remove todas as tags HTML do conteúdo gerado para obter o texto puro
        textContent=strip_tags(htmlContent)

        #cria uma nova instância de EmailMessage com os parâmetros definidos
        email=EmailMessage(
            #completa o subject do email
            subject=f"Novo filme disponível: {movie.title}",
            #conteúdo em texto puro (sem HTML)
            body=textContent,
            from_email='cinepass.p3@gmail.com',
            #puxa o email do usuario que estamos percorrendo no for
            to=[user.user.email]
        )
        #define que o corpo do email vai ser enviado como html
        email.content_subtype='html'
        email.send()
        
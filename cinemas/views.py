from django.shortcuts import render
from .models import Cinema, Room
from .forms import CinemaForm, RoomForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def index(request):
    return render(request, 'cinemas/index.html')

# @login_required faz com que apenas usuários que estejam logados possam acessar
@login_required
def cinemas(request):
    #Resgata todos os cinemas para listagem
    cinemas=Cinema.objects.order_by('dateAdded')
    context={'cinemas':cinemas}
    return render(request, 'cinemas/cinemas.html', context)

# essa função vai retornar o cinema com o id especificado no request
@login_required
def cinema(request, cinemaId):
    #tratamento para o caso de o id do cinema não retornar nada
    try:
        cinema = Cinema.objects.get(id=cinemaId)
    except Cinema.DoesNotExist:
        return HttpResponseNotFound("Cinema não encontrado")
    
    #listagem de salas do cinema escolhido
    rooms = cinema.room_set.order_by('dateAdded')
    context = {'cinema': cinema, 'rooms': rooms, 'cinemaId': cinemaId}
    return render(request, 'cinemas/cinema.html', context)

@login_required
def newCinema(request):
    #se o metodo for 'GET', significa que o formulário esta sendo carregado, portanto um form vazio é criado
    if request.method!='POST':
        form=CinemaForm()
    else:
    #se o metodo for 'POST', instancia o form com os dados do usuário
        form=CinemaForm(request.POST)
        #verifica se todos os campos foram preenchidos corretamente
        if form.is_valid():
            try:
                #se for tudo válido, vai tentar salvar no banco
                form.save()
                return HttpResponseRedirect(reverse('cinemas'))
            except IntegrityError:
                #caso tenha algum problema durante o salvamento, esse erro aparece
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    #caso tenha algum erro novo ou inesperado
                    form.add_error(None, f"Erro inesperado: {e}")

    context={'form':form}
    return render(request, 'cinemas/newCinema.html', context)

@login_required
def newRoom(request, cinemaId):
    # vai funcionar semelhante ao newCinema com exceção do fato de que primeiro temos que pegar o id no request do cinema para adicionar a sala
    # já que cada sala está associada a um cinema
    try:
        #vai tentar achar o cinema com o id passado e atribuir à variável cinema
        cinema = Cinema.objects.get(id=cinemaId)
    except Cinema.DoesNotExist:
        return HttpResponseNotFound("Item não encontrado")

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            #vai salvar as informações no newRoom e já vai atribuir o cinema para que o usuario nao precise preencher
            newRoom = form.save(commit=False)
            newRoom.cinema = cinema
            try:
                #vai tentar salvar o novo objeto
                newRoom.save()
                #caso salve, irá voltar para tela do cinema do qual a sala foi adicionada
                return HttpResponseRedirect(reverse('cinema', args=[cinemaId]))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form = RoomForm()
    
    context = {'cinema': cinema, 'form': form, 'cinemaId': cinemaId}
    return render(request, 'cinemas/newRoom.html', context)

@login_required
def editCinema(request, cinemaId):
    try:
        #procura o cinema que corresponde o id do request e salva na variavel cinema para ser editado
        cinema = Cinema.objects.get(id=cinemaId)
    except Cinema.DoesNotExist:
        return HttpResponseNotFound("Item não encontrado")

    if request.method=='POST':
        #vai completar com as informações do próprio objeto para que o usuario altere o que for necessário e se o metodo
        #for post, pega as informações que estiverem no form
        form=CinemaForm(instance=cinema, data=request.POST)
        if form.is_valid():
            try:
                #tenta salvar as alterações
                form.save()
                return HttpResponseRedirect(reverse('cinemas'))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        #preenche o form com os dados do proprio objeto
        form=CinemaForm(instance=cinema)
    
    context={'cinema':cinema, 'form': form}
    return render(request, 'cinemas/editCinema.html', context)

@login_required
def editRoom(request, roomId):
    #mesma lógica do editCinema, exceto que não podemos alterar apenas o id do cinema da sala
    room=Room.objects.get(id=roomId)
    #vai associar o id do cinema associada à sala à variavel 
    cinemaId = room.cinema.id
    try:
        #procura o cinema da sala que queremos editar
        cinema = Cinema.objects.get(id=cinemaId)
    except Cinema.DoesNotExist:
        return HttpResponseNotFound("Cinema não encontrado")

    if request.method=='POST':
        #mesma lógica do editCinema
        form=RoomForm(instance=room, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect(reverse('cinema', args=[cinema.id]))
            except IntegrityError:
                form.add_error(None, "Erro ao salvar. Dados duplicados ou violação de integridade")
            except Exception as e:
                    form.add_error(None, f"Erro inesperado: {e}")
    else:
        form=RoomForm(instance=room)
    
    context={'room':room, 'cinema':cinema, 'form': form}
    return render(request, 'cinemas/editRoom.html', context)

@login_required
def deleteCinema(request, cinemaId):
    try:
        #puxa o cinema que corresponde ao Id passado no request
        cinema = Cinema.objects.get(id=cinemaId)
    except Cinema.DoesNotExist:
        return HttpResponseNotFound("Cinema não encontrado")

    if request.method == 'POST':
        #executa o metodo delete
        cinema.delete()
        return HttpResponseRedirect(reverse('cinemas'))
    
    context = {'cinema': cinema}
    return render(request, 'cinemas/deleteCinema.html', context)

@login_required
def deleteRoom(request, roomId):
    try:
        #puxa a sala que é passada no request
        room = Room.objects.get(id=roomId)
    except Room.DoesNotExist:
        return HttpResponseNotFound("Sala não encontrada")

    #puxa o cinema que está associado à sala para usar no HttpResponseRedirect depois
    cinema = room.cinema

    if request.method == 'POST':
        room.delete()
        return HttpResponseRedirect(reverse('cinema', args=[cinema.id]))

    context = {'room': room, 'cinema': cinema}
    return render(request, 'cinemas/deleteRoom.html', context)
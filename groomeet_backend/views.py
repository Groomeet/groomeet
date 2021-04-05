from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from groomeet_backend.models import *
from django.contrib.auth import login, logout,authenticate

# Create your views here.
from django.shortcuts import render

def index(request):
    context = listadoMusicos(request)
    return render(request, '../templates/index.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

def chat(request):
    return render(request, 'chat.html')

def getMusico(request, id):
    musico = Musico.objects.get(id=id)
    nombre = musico.usuario.username + ";"
    fechaNac = str(musico.fechaNacimiento) + ";"
    id = str(musico.id)

    response = nombre + fechaNac + id
    return HttpResponse(response)

def getBanda(request, id):
    banda = Banda.objects.get(id=id)
    nombre = banda.nombre + ";"
    id = str(banda.id)

    response = nombre + id
    return HttpResponse(response)


def listadoMusicos(request):
    musicos = Musico.objects.all()
    result = []
    usuario = request.user
    for musico in musicos:
        if usuario.id is not musico.usuario.id and usuario not in musico.likesRecibidos.all() and usuario not in musico.noLikesRecibidos.all():
            result.append(musico)
    context = {
        'musicos': result,
        'usuario': usuario,
    }
    return context

def listadoBandas(request):
    bandas = Banda.objects.all()
    result = []
    usuario = request.user
    for banda in bandas:
        if usuario.id is not banda.administrador.id and usuario not in banda.likesRecibidosMusico.all() and usuario not in banda.noLikesRecibidosMusico.all():
            result.append(banda)
    context = {
        'bandas': result,
        'usuario': usuario,
    }
    return context

def listadoBandasMusicos(request, pkBanda):
    musicos = Musico.objects.all()
    banda = get_object_or_404(Banda, id=pkBanda)
    result = []
    usuario = request.user
    for musico in musicos:
        if banda.administrador.id is not musico.id and musico not in banda.miembros.all() and banda not in musico.likesRecibidosBanda.all() and banda not in musico.noLikesRecibidosBanda.all():
            result.append(musico)
    context = {
        'musicos': result,
        'usuario': usuario,
        'pkBanda': pkBanda,
    }
    return render(request, "../templates/listadoBandasMusicos.html", context)

def listadoBandasBandas(request, pkBanda):
    bandas = Banda.objects.all()
    banda = get_object_or_404(Banda, id=pkBanda)
    result = []
    usuario = request.user
    for b in bandas:
        if usuario.id is not b.administrador.usuario.id and banda not in b.likesRecibidosBanda.all() and banda not in b.noLikesRecibidosBanda.all():
            result.append(b)
    context = {
        'bandas': result,
        'usuario': usuario,
        'pkBanda': pkBanda,
    }
    return render(request, "../templates/listadoBandasBandas.html", context)


def listadoMisBandas(request):
    misBandas = Banda.objects.all().filter(administrador=request.user.musico).order_by('-nombre')
    return render(request, "misBandas.html", {'misBandas': misBandas})

def listadoMiembrosNoRegistrados(request):
    misMiembrosNoRegistrados = MiembroNoRegistrado.objects.all().filter(banda=request.user.pk).order_by('-nombre')
    return render(request, "misBandas.html", {'misMiembrosNoRegistrados': misMiembrosNoRegistrados})

def listadoGeneros(request):
    currentUser = Musico.objects.get(id=request.user.pk)
    generos = Genero.objects.all()
    context = {'generos': generos}
    return render(request, '../templates/generos.html', context)

def listadoMisInvitaciones(request):
    misInvitaciones = Invitacion.objects.all().filter(receptor=request.user.musico)
    return render(request, "misInvitaciones.html", {'misInvitaciones': misInvitaciones})

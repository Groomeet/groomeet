from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from groomeet_backend.likes import postUndoLikeMusicoMusico
from groomeet_backend.models import *
from django.contrib.auth import logout,authenticate
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.
def base(request):
    return render(request, 'base.html')


def days_between(d1, d2):
    return abs(d2 - d1).days

@login_required(login_url='/login/')
def index(request):

    context = listadoMusicos(request)
    return render(request, '../templates/index.html', context)

@login_required(login_url='/login/')
def musico(request):
    if request.user.musico.isGold==False and request.user.musico.isSilver==False:
        fechaUltimaRenovacion = request.user.musico.ultimaRenovacionLikes
        today = date.today()
        dias = days_between(fechaUltimaRenovacion, today)
        if dias >= 1:
            request.user.musico.likesDisponibles = 10
            request.user.musico.ultimaRenovacionLikes = today
            request.user.musico.save()
    try:
        compra = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra').first()
        today = date.today()
        dias = days_between(compra.fecha_compra, today)
        if(dias>30):
            request.user.musico.isGold=False
            request.user.musico.isSilver=False
            request.user.musico.save()
    except:
        pass
    ruta = request.path
    musico = Musico.objects.get(usuario=request.user)

    if(ruta == "/"):
        url = ""
    elif(ruta == "buscarBandas"):
        "Buscando bandas como músico"
    return render(request, '../templates/index.html')

@login_required(login_url='/login/')
def banda(request, pkBanda):
    banda = get_object_or_404(Banda, id=pkBanda) #ESTO HAY QUE DARLE UN REPASO
    usuario = request.user
    if (banda.administrador.id == usuario.id):
        return render(request, '../templates/index.html')
    else:
        return redirect("/")

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def chat(request):
    return render(request, 'chat.html')

@login_required(login_url='/login/')
def getMusico(request):
    musicos = Musico.objects.all().order_by('-isBoosted', '-usuario__last_login')
    result = []
    usuario = request.user

    for musico in musicos:
        if usuario.id is not musico.usuario.id and usuario not in musico.likesRecibidos.all() and usuario not in musico.noLikesRecibidos.all():
            result.append(musico)

    musico = result[0]
    nombre = musico.usuario.username + ";"
    generosList = musico.generos.values_list("nombre", flat=True)
    generos = ", ".join(generosList) + ";"
    video = musico.enlaceVideo + ";"
    id = str(musico.id)

    response = nombre + generos + video + id
    print(response)
    return HttpResponse(response)

@login_required(login_url='/login/')
def getMusico2(request, pkBanda):
    musicos = Musico.objects.all()
    result = []
    banda = get_object_or_404(Banda, id=pkBanda) #ESTO HAY QUE DARLE UN REPASO
    for musico in musicos:
        if banda.administrador.id is not musico.id and musico not in banda.miembros.all() and banda not in musico.likesRecibidosBanda.all() and banda not in musico.noLikesRecibidosBanda.all():
            result.append(musico)

    musico = result[0]
    nombre = musico.usuario.username + ";"
    generosList = musico.generos.values_list("nombre", flat=True)
    generos = ", ".join(generosList) + ";"
    video = musico.enlaceVideo + ";"
    id = str(musico.id)

    response = nombre + generos + video + id
    print(response)
    return HttpResponse(response)

@login_required(login_url='/login/')
def getBanda(request):
    bandas = Banda.objects.all()
    result = []
    user = request.user
    musico = Musico.objects.get(usuario=user)
    for banda in bandas:
        if musico.id is not banda.administrador.id and user not in banda.likesRecibidosMusico.all() and user not in banda.noLikesRecibidosMusico.all():
            result.append(banda)
    banda = result[0]
    nombre = banda.nombre + ";"
    generosList = banda.generos.values_list("nombre", flat=True)
    generos = ", ".join(generosList) + ";"
    video = "https://www.youtube.com/embed/0hEYvdMoF2g" + ";"
    id = str(banda.id)

    response = nombre + generos + video + id
    return HttpResponse(response)

@login_required(login_url='/login/')
def getBanda2(request, pkBanda):
    bandas = Banda.objects.all()
    result = []
    banda = get_object_or_404(Banda, id=pkBanda) #ESTO HAY QUE DARLE UN REPASO
    usuario = request.user
    for b in bandas:
        if usuario.id is not b.administrador.usuario.id and banda not in b.likesRecibidosBanda.all() and banda not in b.noLikesRecibidosBanda.all():
            result.append(b)
    banda = result[0]
    nombre = banda.nombre + ";"
    generosList = banda.generos.values_list("nombre", flat=True)
    generos = ", ".join(generosList) + ";"
    video = "https://www.youtube.com/embed/0hEYvdMoF2g" + ";"
    id = str(banda.id)

    response = nombre + generos + video + id
    return HttpResponse(response)

@login_required(login_url='/login/')
def listadoMusicos(request):
    musicos = Musico.objects.all().order_by('-isBoosted')
    result = []
    usuario = request.user
    for musico in musicos:
        if usuario.id is not musico.usuario.id and usuario not in musico.likesRecibidos.all() and usuario not in musico.noLikesRecibidos.all():
            result.append(musico)
    print(result)        
    context = {
        'musicos': result,
        'usuario': usuario,
    }

    return context

@login_required(login_url='/login/')
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
    return render(request, "../templates/listadoBandas.html", context)

@login_required(login_url='/login/')
def listadoBandasMusicos(request, pkBanda):
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if(banda.administrador == usuario):
        musicos = Musico.objects.all()
        result = []
        for musico in musicos:
            if banda.administrador.id is not musico.id and musico not in banda.miembros.all() and banda not in musico.likesRecibidosBanda.all() and banda not in musico.noLikesRecibidosBanda.all():
                result.append(musico)
        context = {
            'musicos': result,
            'usuario': usuario,
            'pkBanda': pkBanda,
        }
        return render(request, "../templates/listadoBandasMusicos.html", context)
    else:
        return redirect("/")
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def listadoMisBandas(request):
    misBandas = Banda.objects.all().filter(administrador=request.user.musico).order_by('-nombre')
    return render(request, "misBandas.html", {'misBandas': misBandas})

@login_required(login_url='/login/')
def listadoMiembrosNoRegistrados(request):
    misMiembrosNoRegistrados = MiembroNoRegistrado.objects.all().filter(banda=request.user.pk).order_by('-nombre')
    return render(request, "misBandas.html", {'misMiembrosNoRegistrados': misMiembrosNoRegistrados})

@login_required(login_url='/login/')
def listadoGeneros(request):
    currentUser = Musico.objects.get(id=request.user.pk)
    generos = Genero.objects.all()
    context = {'generos': generos}
    return render(request, '../templates/generos.html', context)

@login_required(login_url='/login/')
def listadoMisInvitaciones(request):
    misInvitaciones = Invitacion.objects.all().filter(receptor=request.user.musico)
    return render(request, "misInvitaciones.html", {'misInvitaciones': misInvitaciones})

@login_required(login_url='/login/')
def chat_room(request, room_name):
    return render(request, 'chat_room.html', {
        'room_name': room_name
})
from django.shortcuts import render
from groomeet_backend.models import *

# Create your views here.

def index(request):
    return render(request, '../templates/index.html')

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
    return render(request, "../templates/listado.html", context)

def listadoMisBandas(request):
    misBandas = Banda.objects.all().filter(administrador=request.user.pk).order_by('-nombre')
    return render(request, "misBandas.html", {'misBandas': misBandas})

def listadoMiembrosNoRegistrados(request):
    misMiembrosNoRegistrados = MiembroNoRegistrado.objects.all().filter(banda=request.user.pk).order_by('-nombre')
    return render(request, "misBandas.html", {'misMiembrosNoRegistrados': misMiembrosNoRegistrados})
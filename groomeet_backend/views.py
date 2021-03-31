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
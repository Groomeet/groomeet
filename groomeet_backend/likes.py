from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from groomeet_backend.models import Musico
from django.contrib.auth.decorators import login_required

@login_required
def postLike(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if musico.usuario.id is usuario.id:
        redirect("/listado")
    if usuario in musico.likesRecibidos.all():
        musico.likesRecibidos.remove(usuario)
    else:
        musico.likesRecibidos.add(usuario)
        if musico.usuario in usuario.musico.likesRecibidos.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {musico.usuario.username} también le gustaste")
            print(f"¡Eso fue un match!, a {musico.usuario.username} también le gustaste")
    return redirect("/listado")

@login_required
def postNoLike(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if usuario not in musico.noLikesRecibidos.all():
        musico.noLikesRecibidos.add(usuario)

    return redirect("/listado")
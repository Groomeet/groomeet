from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from groomeet_backend.models import Musico, Banda, Chat
from django.contrib.auth.decorators import login_required


#Sección de likes y no likes entre músicos
@login_required
def postLikeMusicoMusico(request, pk):
    print(pk)
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
            url = "/chat/" + usuario.id + "-" + musico.usuario.id
            print(url)
            chat = Chat.objects.create(nombre = url)
            print(chat)
            musico.chat.add(chat)
            usuario.musico.chat.add(chat)            
            print(f"¡Eso fue un match!, a {musico.usuario.username} también le gustaste")
    return HttpResponse("Post correcto.")


@login_required
def postNoLikeMusicoMusico(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if usuario not in musico.noLikesRecibidos.all():
        musico.noLikesRecibidos.add(usuario)

    return HttpResponse("Post correcto.")

#Sección de likes y no likes de músicos a bandas
@login_required
def postLikeMusicoBanda(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if banda.administrador.id is usuario.id:
        redirect("/listadoBandas")
    if usuario in banda.likesRecibidosMusico.all():
        banda.likesRecibidosMusico.remove(usuario)
    else:
        banda.likesRecibidosMusico.add(usuario)
        if banda in usuario.musico.likesRecibidosBanda.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {banda.nombre} también le gustaste")
            print(f"¡Eso fue un match!, a {banda.nombre} también le gustaste")
    return HttpResponse("Post correcto.")

@login_required
def postNoLikeMusicoBanda(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if usuario not in banda.noLikesRecibidosMusico.all():
        banda.noLikesRecibidosMusico.add(usuario)

    return HttpResponse("Post correcto.")

#Sección de likes y no likes de bandas a musicos
@login_required
def postLikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if banda.administrador.id != usuario.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if banda in musico.likesRecibidosBanda.all():
        musico.likesRecibidosBanda.remove(banda)
    else:
        musico.likesRecibidosBanda.add(banda)
        if musico in banda.likesRecibidosMusico.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {musico.usuario.username} también le gustasteis")
            print(f"¡Eso fue un match!, a {musico.usuario.username} también le gustasteis")
    return HttpResponse("Post correcto.")

@login_required
def postNoLikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if banda.administrador.id != usuario.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if banda not in musico.noLikesRecibidosBanda.all():
        musico.noLikesRecibidosBanda.add(banda)

    return HttpResponse("Post correcto.")

#Sección de likes y no likes entre bandas 
@login_required
def postLikeBandaBanda(request, pkEmisor, pkReceptor):
    bandaEmisora = get_object_or_404(Banda, id=pkEmisor)
    bandaReceptora = get_object_or_404(Banda, id=pkReceptor)
    usuario = request.user
    if bandaEmisora.administrador.id != usuario.id:
        redirect("/misBandas")
    if bandaEmisora.administrador.id is bandaReceptora.administrador.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.id is bandaReceptora.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora in bandaReceptora.likesRecibidosBanda.all():
        bandaReceptora.likesRecibidosBanda.remove(bandaEmisora)
    else:
        bandaReceptora.likesRecibidosBanda.add(bandaEmisora)
        if bandaReceptora in bandaEmisora.likesRecibidosBanda.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {bandaReceptora.nombre} también le gustasteis")
            print(f"¡Eso fue un match!, a {bandaReceptora.nombre} también le gustasteis")
    return HttpResponse("Post correcto.")

@login_required
def postNoLikeBandaBanda(request, pkEmisor, pkReceptor):
    bandaEmisora = get_object_or_404(Banda, id=pkEmisor)
    bandaReceptora = get_object_or_404(Banda, id=pkReceptor)
    usuario = request.user
    if bandaEmisora.administrador.id != usuario.id:
        redirect("/misBandas")
    if bandaEmisora.administrador.id is bandaReceptora.administrador.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.id is bandaReceptora.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora not in bandaReceptora.noLikesRecibidosBanda.all():
        bandaReceptora.noLikesRecibidosBanda.add(bandaEmisora)

    return HttpResponse("Post correcto.")

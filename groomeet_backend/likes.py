from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from rest_framework import status

from groomeet_backend.models import Musico, Banda, Chat
from django.contrib.auth.decorators import login_required


#Sección de likes y no likes entre músicos
@login_required(login_url='/login/')
def postLikeMusicoMusico(request, pk):
    print(pk)
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if musico.usuario.id is usuario.id:
        redirect("/listado")
    if usuario in musico.likesRecibidos.all():
        musico.likesRecibidos.remove(usuario)
    if not usuario.musico.isGold and not usuario.musico.isSilver and usuario.musico.likesDisponibles <= 0:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    else:
        musico.likesRecibidos.add(usuario)
        usuario.musico.likesDisponibles = usuario.musico.likesDisponibles -1
        usuario.musico.ultimoUsuarioInteraccion.clear()
        usuario.musico.ultimoUsuarioInteraccion.add(musico.usuario)
        usuario.musico.save()
        if musico.usuario in usuario.musico.likesRecibidos.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {musico.usuario.username} también le gustaste")
            url = "/chat/" + str(usuario.id) + "-" + str(musico.usuario.id)
            print(url)
            chat = Chat.objects.create(nombre = url)
            print(chat)
            musico.chat.add(chat)
            usuario.musico.chat.add(chat)            
            print(f"¡Eso fue un match!, a {musico.usuario.username} también le gustaste")
    return HttpResponse("Post correcto.")


@login_required(login_url='/login/')
def postNoLikeMusicoMusico(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if usuario not in musico.noLikesRecibidos.all():
        musico.noLikesRecibidos.add(usuario)
        usuario.musico.ultimoUsuarioInteraccion.clear()
        usuario.musico.ultimoUsuarioInteraccion.add(musico.usuario)

    return HttpResponse("Post correcto.")

#Sección de likes y no likes de músicos a bandas
@login_required(login_url='/login/')
def postLikeMusicoBanda(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if banda.administrador.id is usuario.id:
        redirect("/listadoBandas")
    if usuario in banda.likesRecibidosMusico.all():
        banda.likesRecibidosMusico.remove(usuario)
    if not usuario.musico.isGold and not usuario.musico.isSilver and usuario.musico.likesDisponibles <= 0:
        #mensaje = "Has agotado tus likes" 
        #return render(request, '../templates/index.html', {'mensaje': mensaje})
        #Cambiar a un mensaje/vista de que compre una suscripción
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    else:
        banda.likesRecibidosMusico.add(usuario)
        usuario.musico.likesDisponibles = usuario.musico.likesDisponibles -1
        usuario.musico.ultimoUsuarioInteraccion.clear()
        usuario.musico.ultimoUsuarioInteraccion.add(banda.administrador.usuario)
        usuario.musico.save()
        if banda in usuario.musico.likesRecibidosBanda.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {banda.nombre} también le gustaste")
            url = "/chat/" + str(usuario.id) + "-" + str(banda.administrador.usuario.id)
            print(url)
            chat = Chat.objects.create(nombre = url)
            print(chat)
            banda.administrador.chat.add(chat)
            usuario.musico.chat.add(chat)
            print(f"¡Eso fue un match!, a {banda.nombre} también le gustaste")
    return HttpResponse("Post correcto.")

@login_required(login_url='/login/')
def postNoLikeMusicoBanda(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if usuario not in banda.noLikesRecibidosMusico.all():
        banda.noLikesRecibidosMusico.add(usuario)
        usuario.musico.ultimoUsuarioInteraccion.clear()
        usuario.musico.ultimoUsuarioInteraccion.add(banda.administrador.usuario)
        usuario.musico.save()
        
    return HttpResponse("Post correcto.")

#Sección de likes y no likes de bandas a musicos
@login_required(login_url='/login/')
def postLikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if banda.administrador.id != usuario.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if not usuario.musico.isGold and not usuario.musico.isSilver and usuario.musico.likesDisponibles <= 0:
        #mensaje = "Has agotado tus likes" 
        #return render(request, '../templates/index.html', {'mensaje': mensaje})
        #Cambiar a un mensaje/vista de que compre una suscripción
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if banda in musico.likesRecibidosBanda.all():
        musico.likesRecibidosBanda.remove(banda)
    
    else:
        musico.likesRecibidosBanda.add(banda)
        usuario.musico.likesDisponibles = usuario.musico.likesDisponibles -1
        banda.administrador.ultimoUsuarioInteraccion.clear()
        banda.administrador.ultimoUsuarioInteraccion.add(usuario)
        banda.administrador.save()
        usuario.musico.save()
        if musico in banda.likesRecibidosMusico.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {musico.usuario.username} también le gustasteis")
            url = "/chat/" + str(usuario.id) + "-" + str(musico.usuario.id)
            print(url)
            chat = Chat.objects.create(nombre = url)
            print(chat)
            musico.chat.add(chat)
            usuario.musico.chat.add(chat)
            print(f"¡Eso fue un match!, a {musico.usuario.username} también le gustasteis")
    return HttpResponse("Post correcto.")

@login_required(login_url='/login/')
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
        banda.administrador.ultimoUsuarioInteraccion.clear()
        banda.administrador.ultimoUsuarioInteraccion.add(usuario)
        banda.administrador.save()

    return HttpResponse("Post correcto.")

#Sección de likes y no likes entre bandas 
@login_required(login_url='/login/')
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
    if not usuario.musico.isGold and not usuario.musico.isSilver and usuario.musico.likesDisponibles <= 0:
        #mensaje = "Has agotado tus likes" 
        #return render(request, '../templates/index.html', {'mensaje': mensaje})
        #Cambiar a un mensaje/vista de que compre una suscripción
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if bandaEmisora in bandaReceptora.likesRecibidosBanda.all():
        bandaReceptora.likesRecibidosBanda.remove(bandaEmisora)
    else:
        bandaReceptora.likesRecibidosBanda.add(bandaEmisora)
        usuario.musico.likesDisponibles = usuario.musico.likesDisponibles -1
        bandaEmisora.administrador.ultimoUsuarioInteraccion.clear()
        bandaEmisora.administrador.ultimoUsuarioInteraccion.add(usuario)
        bandaEmisora.administrador.save()
        usuario.musico.save()
        if bandaReceptora in bandaEmisora.likesRecibidosBanda.all():
            #Aquí se uniría la creación del chat
            messages.success(request, f"¡Eso fue un match!, a {bandaReceptora.nombre} también le gustasteis")
            url = "/chat/" + str(bandaEmisora.administrador.usuario.id) + "-" + str(bandaReceptora.administrador.usuario.id)
            print(url)
            chat = Chat.objects.create(nombre = url)
            print(chat)
            bandaEmisora.administrador.chat.add(chat)
            bandaReceptora.administrador.chat.add(chat)
            print(f"¡Eso fue un match!, a {bandaReceptora.nombre} también le gustasteis")
    return HttpResponse("Post correcto.")

@login_required(login_url='/login/')
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
        bandaEmisora.administrador.ultimoUsuarioInteraccion.clear()
        bandaEmisora.administrador.ultimoUsuarioInteraccion.add(usuario)
        bandaEmisora.administrador.save()

    return HttpResponse("Post correcto.")


@login_required(login_url='/login/')
def postSuperLikeMusicoMusico(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if musico.usuario.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if request.user.musico.isGold and request.user.musico.superLikes <= 0:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if musico.usuario in usuario.musico.likesRecibidos.all():
        usuario.musico.likesRecibidos.remove(musico.usuario)
    musico.likesRecibidos.add(usuario)
    usuario.musico.likesRecibidos.add(musico.usuario)
    usuario.musico.superLikes = usuario.musico.superLikes-1
    usuario.musico.save()
    messages.success(request, f"¡Eso fue un superlike!, te encantó {musico.usuario.username}")
    url = "/chat/" + str(usuario.id) + "-" + str(musico.usuario.id)
    chat = Chat.objects.create(nombre = url)
    musico.chat.add(chat)
    usuario.musico.chat.add(chat)            
    print(f"¡Eso fue un superlike!, te encantó {musico.usuario.username}")
    return HttpResponse("Post correcto.")



@login_required(login_url='/login/')
def postSuperLikeMusicoBanda(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if banda.administrador.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if request.user.musico.isGold and request.user.musico.superLikes <= 0:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if banda.administrador.id is usuario.musico.id or usuario.musico in banda.miembros.all():
        redirect("/listadoBandas")
    if banda.administrador in usuario.musico.likesRecibidosBanda.all():
        usuario.musico.likesRecibidosBanda.remove(banda)
    banda.likesRecibidosMusico.add(usuario)
    usuario.musico.likesRecibidosBanda.add(banda)
    usuario.musico.superLikes = usuario.musico.superLikes-1
    usuario.musico.save()
    messages.success(request, f"¡Eso fue un superlike!, te encantó {banda.nombre}")
    url = "/chat/" + str(usuario.id) + "-" + str(banda.administrador.usuario.id)
    chat = Chat.objects.create(nombre = url)
    banda.administrador.chat.add(chat)
    usuario.musico.chat.add(chat)            
    print(f"¡Eso fue un superlike!, te encantó {banda.nombre}")
    return HttpResponse("Post correcto.")


@login_required(login_url='/login/')
def postSuperLikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if banda.administrador.id != usuario.musico.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if request.user.musico.isGold and request.user.musico.superLikes <= 0:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if banda in musico.likesRecibidosBanda.all():
        musico.likesRecibidosBanda.remove(banda)
    banda.likesRecibidosMusico.add(musico.usuario)
    musico.likesRecibidosBanda.add(banda)
    usuario.musico.superLikes = usuario.musico.superLikes-1
    usuario.musico.save()
    messages.success(request, f"¡Eso fue un superlike!, te encantó {musico.usuario.username}")
    url = "/chat/" + str(banda.administrador.usuario.id) + "-" + str(musico.usuario.id)
    chat = Chat.objects.create(nombre = url)
    banda.administrador.chat.add(chat)
    usuario.musico.chat.add(chat)            
    print(f"¡Eso fue un superlike!, te encantó {banda.nombre}")
    return redirect(f'/listadoBandasMusicos/{pkBanda}')

@login_required(login_url='/login/')
def postSuperLikeBandaBanda(request, pkEmisor, pkReceptor):
    bandaEmisora = get_object_or_404(Banda, id=pkEmisor)
    bandaReceptora = get_object_or_404(Banda, id=pkReceptor)
    usuario = request.user
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if request.user.musico.isGold and request.user.musico.superLikes <= 0:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if bandaEmisora.administrador.id != usuario.id:
        redirect("/misBandas")
    if bandaEmisora.administrador.id is bandaReceptora.administrador.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.id is bandaReceptora.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora in bandaReceptora.likesRecibidosBanda.all():
        bandaReceptora.likesRecibidosBanda.remove(bandaEmisora)
        
    bandaReceptora.likesRecibidosBanda.add(bandaEmisora)
    bandaEmisora.likesRecibidosBanda.add(bandaReceptora)
    usuario.musico.superLikes = usuario.musico.superLikes-1
    usuario.musico.save()
    #Aquí se uniría la creación del chat
    messages.success(request, f"¡Eso fue un superlike!, os encantó {bandaReceptora.nombre}")
    url = "/chat/" + str(bandaEmisora.administrador.usuario.id) + "-" + str(bandaReceptora.administrador.usuario.id)
    chat = Chat.objects.create(nombre = url)
    bandaEmisora.administrador.chat.add(chat)
    bandaReceptora.administrador.chat.add(chat)
    print(f"¡Eso fue un superlike!, os encantó {bandaReceptora.nombre}")
    return redirect(f'/buscarBandas/{pkEmisor}')

@login_required(login_url='/login/')
def postUndoDislikeMusicoMusico(request, pk):
    print(pk)
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if musico.usuario.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario in musico.noLikesRecibidos.all():
        musico.noLikesRecibidos.remove(usuario)
        usuario.musico.save()

        nombre = musico.usuario.username + ";"
        generosList = musico.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = musico.enlaceVideo + ";"
        id = str(musico.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoDislikeMusicoBanda(request, pk):
    print(pk)
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if banda.administrador.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario in banda.noLikesRecibidosMusico.all():
        banda.noLikesRecibidosMusico.remove(usuario)
        usuario.musico.save()

        nombre = banda.nombre + ";"
        generosList = banda.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = banda.enlaceVideo + ";"
        id = str(banda.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoDislikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user

    if banda.administrador.id != usuario.musico.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario.id is banda.administrador.id and banda in musico.noLikesRecibidosBanda.all():
        musico.noLikesRecibidosBanda.remove(banda.id)
        usuario.musico.save()

        nombre = musico.usuario.username + ";"
        generosList = musico.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = musico.enlaceVideo + ";"
        id = str(musico.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoDislikeBandaBanda(request, pkEmisor, pkReceptor):
    bandaEmisora = get_object_or_404(Banda, id=pkEmisor)
    bandaReceptora = get_object_or_404(Banda, id=pkReceptor)
    usuario = request.user

    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if bandaEmisora.administrador.id != usuario.id:
        redirect("/misBandas")
    if bandaEmisora.administrador.id is bandaReceptora.administrador.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.id is bandaReceptora.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.administrador.id is not bandaReceptora.administrador.id and bandaEmisora in bandaReceptora.noLikesRecibidosBanda.all():
        bandaReceptora.noLikesRecibidosBanda.remove(bandaEmisora)

        nombre = bandaReceptora.nombre + ";"
        generosList = bandaReceptora.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = bandaReceptora.enlaceVideo + ";"
        id = str(bandaReceptora.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoLikeMusicoMusico(request, pk):
    musico = get_object_or_404(Musico, id=pk)
    usuario = request.user
    if musico.usuario.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario in musico.likesRecibidos.all():
        musico.likesRecibidos.remove(usuario)
        usuario.musico.save()

        nombre = musico.usuario.username + ";"
        generosList = musico.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = musico.enlaceVideo + ";"
        id = str(musico.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoLikeMusicoBanda(request, pk):
    print(pk)
    banda = get_object_or_404(Banda, id=pk)
    usuario = request.user
    if banda.administrador.id is usuario.id:
        redirect("/listado")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario in banda.likesRecibidosMusico.all():
        banda.likesRecibidosMusico.remove(usuario)
        usuario.musico.save()

        nombre = banda.nombre + ";"
        generosList = banda.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = banda.enlaceVideo + ";"
        id = str(banda.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoLikeBandaMusico(request, pkBanda, pkMusico):
    musico = get_object_or_404(Musico, id=pkMusico)
    banda = get_object_or_404(Banda, id=pkBanda)
    usuario = request.user
    if banda.administrador.id != usuario.musico.id:
        redirect("/misBandas")
    if banda.administrador.id is musico.id or musico in banda.miembros.all():
        redirect(f"/listadoBandasMusicos/{pkBanda}")
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if usuario.id is banda.administrador.id and banda in musico.likesRecibidosBanda.all():
        musico.likesRecibidosBanda.remove(banda)
        usuario.musico.save()

        nombre = musico.usuario.username + ";"
        generosList = musico.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = musico.enlaceVideo + ";"
        id = str(musico.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def postUndoLikeBandaBanda(request, pkEmisor, pkReceptor):
    bandaEmisora = get_object_or_404(Banda, id=pkEmisor)
    bandaReceptora = get_object_or_404(Banda, id=pkReceptor)
    usuario = request.user
    if not usuario.musico.isGold:
        return HttpResponse(f"/listadoProductos/", status=status.HTTP_402_PAYMENT_REQUIRED)
    if bandaEmisora.administrador.id != usuario.id:
        redirect("/misBandas")
    if bandaEmisora.administrador.id is bandaReceptora.administrador.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.id is bandaReceptora.id:
        redirect(f"/buscarBandas/{pkEmisor}")
    if bandaEmisora.administrador.id is not bandaReceptora.administrador.id and bandaEmisora in bandaReceptora.likesRecibidosBanda.all():
        bandaReceptora.likesRecibidosBanda.remove(bandaEmisora)

        nombre = bandaReceptora.nombre + ";"
        generosList = bandaReceptora.generos.values_list("nombre", flat=True)
        generos = ", ".join(generosList) + ";"
        video = bandaReceptora.enlaceVideo + ";"
        id = str(bandaReceptora.id)

        response = nombre + generos + video + id
        print(response)
        return HttpResponse(response)
    return HttpResponse("Post incorrecto.", status=status.HTTP_400_BAD_REQUEST)
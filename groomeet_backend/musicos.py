from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from groomeet_backend.form import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

def signUpMusico(request):
    if request.method == "POST":
        formularioMusico = MusicoForm(request.POST)
        formularioUser = UserForm(request.POST)
        if formularioMusico.is_valid() and formularioUser.is_valid():

            user = User.objects.create_user(username = formularioUser.cleaned_data['username'],first_name = formularioUser.cleaned_data['first_name']
                                        ,last_name = formularioUser.cleaned_data['last_name'],email = formularioUser.cleaned_data['email']
                                        ,password = formularioUser.cleaned_data['password'])
            if 'avatar' in request.FILES:
                musico = Musico.objects.create(usuario = user,fechaNacimiento = formularioMusico.cleaned_data['fechaNacimiento']
                                            ,descripcion = formularioMusico.cleaned_data['descripcion'],enlaceVideo = formularioMusico.cleaned_data['enlaceVideo']
                                            ,avatar=request.FILES['avatar'])
            else:
                musico = Musico.objects.create(usuario = user,fechaNacimiento = formularioMusico.cleaned_data['fechaNacimiento']
                                            ,descripcion = formularioMusico.cleaned_data['descripcion'],enlaceVideo = formularioMusico.cleaned_data['enlaceVideo'])
            musico.generos.set(request.POST.getlist('generos'))
            musico.instrumentos.set(request.POST.getlist('instrumentos'))
            
            #Acciones que se toman si se introduce un usuario referido
            referido = username=formularioMusico.cleaned_data['referido']
            if  referido != None and referido != "":
                referente = get_object_or_404(User, username=formularioMusico.cleaned_data['referido'])
                musico.invitadoPor = referente.musico
                musico.save()
                referente.musico.contadorReferidos = referente.musico.contadorReferidos+1

                #AQUI HAY QUE MIRAR
                if(referente.musico.contadorReferidos == 3):
                    referente.musico.contadorReferidos = 0
                    bonificacion = Bonificacion.objects.create(musico = referente.musico)
                    referente.musico.isGold = True
                referente.musico.save()
         
            return HttpResponseRedirect('/')
    else:
        formularioMusico = MusicoForm()
        formularioUser = UserForm()
    return render(request, 'signUpMusico.html', {'formularioMusico': formularioMusico,'formularioUser': formularioUser})

@login_required(login_url='/login/')
def updateProfileMusico(request):
    usuario = request.user
    musico = get_object_or_404(Musico,usuario=usuario)
    imagenMusico = musico.avatar
    formularioMusico = MusicoUpdateForm(initial={'fechaNacimiento': musico.fechaNacimiento,'descripcion': musico.descripcion,
                                            'instrumentos': musico.instrumentos.all,'generos': musico.generos.all,'avatar': musico.avatar,
                                            'enlaceVideo': musico.enlaceVideo})
    formularioUser = UserUpdateForm(initial={'first_name': usuario.first_name,'last_name': usuario.last_name,
                                        'email': usuario.email})
    if request.method == "POST":
        formularioMusico = MusicoUpdateForm(request.POST, instance=musico)
        formularioUser = UserUpdateForm(request.POST, instance=usuario)
        if formularioMusico.is_valid() and formularioUser.is_valid():
            try:
                formularioMusico.save()
                formularioUser.save()
                model = formularioMusico.instance
                #Si existe una nueva imagen, habrá que cambiar la existente por esta.
                if 'avatar' in request.FILES:
                    #Borramos la imagen anterior si existia.
                    if imagenMusico != "" and imagenMusico != None:
                        os.remove(musico.avatar.path)
                    model.avatar = request.FILES['avatar']
                    model.save()
                else:
                #En caso contrario, comprobaremos que el usuario no ha eliminado la imagen que tenía.
                #Si la ha eliminado habrá que borrarla de los datos.
                    if model.avatar == "" or model.avatar == None:
                        try:
                            os.remove(imagenMusico.path)
                        except Exception as e:
                            pass
                model = formularioUser.instance
                messages.success(request, f"¡Tu perfil ha sido modificado con éxito!")
                return HttpResponseRedirect('/')
            except Exception as e:
                pass
    return render(request, 'updateMusico.html', {'formularioMusico': formularioMusico,'formularioUser': formularioUser})
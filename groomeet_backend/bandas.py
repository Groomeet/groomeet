from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from groomeet_backend.form import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

@login_required(login_url='/login/')
def bandaCreate(request):
    if request.method == "POST":
        formulario = BandaForm(request.POST)
        if formulario.is_valid():
            banda = Banda.objects.create(nombre = formulario.cleaned_data['nombre'], administrador=get_object_or_404(Musico,usuario = request.user),
                                        descripcion=formulario.cleaned_data['descripcion'],enlaceVideo = formulario.cleaned_data['enlaceVideo'])
            if 'imagen' in request.FILES:
                banda.imagen = imagen=request.FILES['imagen']
            banda.save()
            banda.generos.set(request.POST.getlist('generos'))
            banda.instrumentos.set(request.POST.getlist('instrumentos'))
            
            return HttpResponseRedirect('/misBandas')
    else:
        formulario = BandaForm()
    return render(request, 'createBanda.html', {'formulario': formulario})

@login_required(login_url='/login/')
def bandaUpdate(request, id):
    banda = get_object_or_404(Banda,id=id)
    musico = get_object_or_404(Musico,usuario=request.user)
    if banda.administrador != musico:
        return redirect('/misBandas')
    imagenBanda = banda.imagen
    form = BandaForm(initial={'nombre': banda.nombre,'descripcion': banda.descripcion,'instrumentos': banda.instrumentos.all,
                            'generos': banda.generos.all,'imagen': banda.imagen,'enlaceVideo': banda.enlaceVideo})
    if request.method == "POST":
        form = BandaForm(request.POST, instance=banda)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                #Si existe una nueva imagen, habrá que cambiar la existente por esta.
                if 'imagen' in request.FILES:
                    #Borramos la imagen anterior si existia.
                    if imagenBanda != "" and imagenBanda != None:
                        os.remove(banda.imagen.path)
                    model.imagen = request.FILES['imagen']
                    model.save()
                else:
                #En caso contrario, comprobaremos que el usuario no ha eliminado la imagen que tenía.
                #Si la ha eliminado habrá que borrarla de los datos.
                    if model.imagen == "" or model.imagen == None:
                        try:
                            os.remove(imagenBanda.path)
                        except Exception as e:
                            pass
                messages.success(request, f"¡Tu banda ha sido modificada con éxito!")
                return HttpResponseRedirect('/misBandas')
            except Exception as e:
                pass
    return render(request, 'updateBanda.html', {'form': form})


@login_required(login_url='/login/')
def bandaDelete(request, id):
    banda = get_object_or_404(Banda,id=id)
    musico = get_object_or_404(Musico,usuario=request.user)
    if banda.administrador != musico:
        return redirect('/misBandas')
    try:
        banda.delete()
    except:
        pass
    return redirect('/misBandas')


@login_required(login_url='/login/')
def miembroNoRegistradoCreate(request, pk):
    banda = get_object_or_404(Banda,id=pk)
    musico = get_object_or_404(Musico,usuario=request.user)
    if banda.administrador != musico:
        return redirect('/misBandas')
    if request.method == "POST":
        formulario = MiembroNoRegistradoForm(request.POST)
        if formulario.is_valid():
            miembro = MiembroNoRegistrado.objects.create(banda = banda, nombre = formulario.cleaned_data['nombre'], 
            descripcion=formulario.cleaned_data['descripcion'])
            miembro.instrumentos.set(request.POST.getlist('instrumentos'))
            
            return HttpResponseRedirect('/misBandas')
    else:
        formulario = MiembroNoRegistradoForm()
    return render(request, 'createMiembroNoRegistrado.html', {'formulario': formulario})

@login_required(login_url='/login/')
def enviarInvitacionBanda(request, banda_id):
    banda = get_object_or_404(Banda, id=banda_id)
    if banda.administrador != request.user.musico:
        return HttpResponseRedirect('/misBandas')
    if request.method == "POST":
        formulario = InvitarBandaForm(request.POST)
        bID = banda_id
        if formulario.is_valid():
            estado = EstadoInvitacion.Pendiente
            usuario = get_object_or_404(User, username=formulario.cleaned_data['receptor'])
            banda = get_object_or_404(Banda, id=banda_id)
            musicoReceptor = get_object_or_404(Musico,usuario=usuario)

            if banda.administrador == musicoReceptor:
                messages.error = (request, f"El usuario {usuario.username} ya pertenece a la banda {banda.nombre}")
                return HttpResponseRedirect('/misBandas')

            #Comprobando que el usuario no pertenece ya a la banda
            if musicoReceptor in banda.miembros.all(): 
                messages.error = (request, f"El usuario {usuario.username} ya pertenece a la banda {banda.nombre}")
                return HttpResponseRedirect('/misBandas')

            #Comprobando que el usuario no tiene ya una invitación pendiente para esa banda
            try:
                invitacion_pendiente = Invitacion.objects.get(receptor = musicoReceptor, 
                                                    banda = banda, estado = EstadoInvitacion.Pendiente)
                messages.error = (request, f"El usuario {usuario.username} ya tiene una invitación pendiente para la banda {banda.nombre}")
            except:
                invitacion_pendiente = None

            if invitacion_pendiente == None:
                invitacion = Invitacion.objects.create(receptor = musicoReceptor, emisor=get_object_or_404(Musico,usuario = request.user),
                                                banda=banda, estado=estado)
                messages.success = (request, f"¡La invitación a {usuario.username} para la banda {banda.nombre} fue enviada!")
            return HttpResponseRedirect('/misBandas')
    else:
        formulario = InvitarBandaForm()
        bID = banda_id
    return render(request, 'invitarBanda.html', {'formulario': formulario,'bID': bID})


@login_required(login_url='/login/')
def aceptarInvitacionBanda(request, invitacion_id):
    usuario = request.user
    receptor = get_object_or_404(Musico, usuario=usuario)
    invitacion = get_object_or_404(Invitacion, id=invitacion_id, receptor = receptor, estado = EstadoInvitacion.Pendiente)

    banda = invitacion.banda
    nuevo_miembro = MiembroDe.objects.create(musico = receptor, banda = banda)
    invitacion.estado = EstadoInvitacion.Aceptada
    invitacion.save()
    messages.success = (request, f"¡Te has unido a la banda {banda.nombre}!")

    return redirect("/misInvitaciones")

@login_required(login_url='/login/')
def rechazarInvitacionBanda(request, invitacion_id):
    usuario = request.user
    receptor = get_object_or_404(Musico, usuario=usuario)
    invitacion = get_object_or_404(Invitacion, id=invitacion_id, receptor = receptor, estado = EstadoInvitacion.Pendiente)

    invitacion.estado = EstadoInvitacion.Rechazada
    invitacion.save()
    messages.success = (request, f"¡Has rechazado la invitación a la banda {invitacion.banda.nombre}!")

    return redirect("/misInvitaciones")

# Este sera el método utilizado para cuando se implemente las invitaciones en el propio chat

@login_required(login_url='/login/')
def eliminarMiembroBanda(request, pkBanda, pkMusico):
    banda = get_object_or_404(Banda, id=pkBanda)
    musico = get_object_or_404(Musico, id=pkMusico)
    usuario = request.user
    if (banda.administrador.usuario.id != usuario.id and usuario.id != musico.usuario.id):
        return redirect("/misBandas")
    banda.miembros.remove(musico)
    return redirect("/misBandas")

@login_required(login_url='/login/')
def eliminarMiembroNoRegistrado(request, pkBanda, pkMiembro):
    banda = get_object_or_404(Banda, id=pkBanda)
    miembroNoRegistrado = get_object_or_404(MiembroNoRegistrado, id=pkMiembro)
    usuario = request.user
    if (banda.administrador.usuario.id != usuario.id):
        return redirect("/misBandas")
    miembroNoRegistrado.delete()
    return redirect("/showBanda/{{ pkBanda }}")
#Este sera el método utilizado para cuando se implemente las invitaciones en el propio chat
'''
@login_required(login_url='/login/')
def enviarInvitacionBanda2(request, receptor_id, banda_id):
    print('metodo')
    emisor = get_object_or_404(Musico, usuario=request.user)
    print(emisor.usuario)
    print(receptor_id)
    recepto = get_object_or_404(User, id=receptor_id)
    print(recepto)
    receptor = get_object_or_404(Musico, usuario_id=receptor_id)
    banda = get_object_or_404(Banda, id=banda_id)
    estado = EstadoInvitacion.Pendiente

    #Comprobando que el usuario no pertenece ya a la banda
    try:
        invitacion_aceptada = Invitacion.objects.get(receptor = receptor, 
                                            banda = banda, estado = EstadoInvitacion.Aceptada)
        messages.error = (request, f"El usuario {receptor.usuario.username} ya pertenece a la banda {banda.nombre}")
    except:
        invitacion_aceptada = None

    #Comprobando que el usuario no tiene ya una invitación pendiente para esa banda
    try:
        invitacion_pendiente = Invitacion.objects.get(receptor = receptor, 
                                            banda = banda, estado = EstadoInvitacion.Pendiente)
        messages.error = (request, f"El usuario {receptor.usuario.username} ya tiene una invitación pendiente para la banda {banda.nombre}")
    except:
        invitacion_pendiente = None

    #Creando la invitacion
    if invitacion_aceptada == None and invitacion_pendiente == None:
        try:
            invitacion = Invitacion.objects.create(emisor = emisor, receptor = receptor, 
                                                banda = banda, estado = estado)
            messages.success = (request, f"¡La invitación a {receptor.usuario.username} para la banda {banda.nombre} fue enviada!")
        except:
            messages.error = (request, f"La invitación no se pudo enviar")
        
    return redirect(request.META['HTTP_REFERER'])
    '''
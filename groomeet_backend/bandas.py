from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from groomeet_backend.form import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def bandaCreate(request):
    if request.method == "POST":
        formulario = BandaForm(request.POST)
        if formulario.is_valid():
            banda = Banda.objects.create(nombre = formulario.cleaned_data['nombre'], administrador=get_object_or_404(Musico,usuario = request.user))
            banda.generos.set(request.POST.getlist('generos'))
            banda.instrumentos.set(request.POST.getlist('instrumentos'))
            
            return HttpResponseRedirect('/misBandas')
    else:
        formulario = BandaForm()
    return render(request, 'createBanda.html', {'formulario': formulario})

@login_required
def bandaUpdate(request, id):
    banda = Banda.objects.get(id=id)
    form = BandaForm(initial={'nombre': banda.nombre})
    if request.method == "POST":
        form = BandaForm(request.POST, instance=banda)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/misBandas')
            except Exception as e:
                pass
    return render(request, 'updateBanda.html', {'form': form})


@login_required
def bandaDelete(request, id):
    banda = Banda.objects.get(id=id)
    try:
        banda.delete()
    except:
        pass
    return redirect('/misBandas')


@login_required
def miembroNoRegistradoCreate(request, pk):
    banda = get_object_or_404(Banda, id=pk)
    if banda.administrador.usuario.id != request.user.id:
        return HttpResponseRedirect('/misBandas')
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

@login_required
def enviarInvitacionBanda(request, receptor_id, banda_id):
    emisor = get_object_or_404(Musico, usuario=request.user)
    receptor = get_object_or_404(Musico, id=receptor_id)
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
        
    return redirect("/listado")

@login_required
def aceptarInvitacionBanda(request, invitacion_id):
    usuario = request.user
    receptor = get_object_or_404(Musico, usuario=usuario)
    invitacion = get_object_or_404(Invitacion, id=invitacion_id, receptor = receptor, estado = EstadoInvitacion.Pendiente)

    banda = invitacion.banda
    nuevo_miembro = MiembroDe.objects.create(musico = receptor, banda = banda)
    invitacion.estado = EstadoInvitacion.Aceptada
    invitacion.save()
    messages.success = (request, f"¡Te has unido a la banda {banda.nombre}!")

    return redirect("/listado")

@login_required
def rechazarInvitacionBanda(request, invitacion_id):
    usuario = request.user
    receptor = get_object_or_404(Musico, usuario=usuario)
    invitacion = get_object_or_404(Invitacion, id=invitacion_id, receptor = receptor, estado = EstadoInvitacion.Pendiente)

    banda = invitacion.banda
    nuevo_miembro = MiembroDe.objects.create(musico = receptor, banda = banda)
    invitacion.estado = EstadoInvitacion.Rechazada
    invitacion.save()
    messages.success = (request, f"¡Has rechazado la invitación a la banda {banda.nombre}!")

    return redirect("/listado")
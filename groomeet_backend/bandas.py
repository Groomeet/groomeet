from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from groomeet_backend.form import *
from django.contrib.auth.decorators import login_required

@login_required
def bandaCreate(request):
    if request.method == "POST":
        formulario = BandaForm(request.POST)
        if formulario.is_valid():
            banda = Banda.objects.create(nombre = formulario.cleaned_data['nombre'], administrador=Musico(request.user.pk))
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
    if banda.administrador.id != request.user.id:
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
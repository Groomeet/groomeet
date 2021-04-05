from groomeet_backend.models import *
from django import forms

class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        exclude =('miembros', 'administrador','likesRecibidosMusico','noLikesRecibidosMusico'
        ,'likesRecibidosBanda','noLikesRecibidosBanda' )

class MiembroNoRegistradoForm(forms.ModelForm):
    class Meta:
        model = MiembroNoRegistrado
        exclude =('banda',)
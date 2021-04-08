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

class InvitarBandaForm(forms.Form):
    receptor = forms.CharField(required=True)

    def clean(self):
        receptor = self.cleaned_data['receptor']
        try:
            usuario = User.objects.get(username=receptor)
        except:
            usuario = None

        if usuario is None:
            raise forms.ValidationError("El usuario que quiere invitar a la banda no existe")
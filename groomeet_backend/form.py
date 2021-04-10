from groomeet_backend.models import *
from django import forms
from datetime import datetime

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

class UserForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellidos")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Contraseña",widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellidos")
    email = forms.EmailField(label="Email")
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class MusicoForm(forms.ModelForm):
    YEARS= [x for x in range(1900,datetime.now().year)]
    fechaNacimiento = forms.DateField(label="Fecha de nacimiento",widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Musico
        fields = ('fechaNacimiento','descripcion','instrumentos','generos','avatar','enlaceVideo')

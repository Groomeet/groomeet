from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel, SoftDeletableModel
from datetime import date
from dateutil.relativedelta import relativedelta
# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

#Añadir ubicaciones para mejora del filtro de búsqueda
class Musico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    instrumentos = models.ManyToManyField(Instrumento)
    generos = models.ManyToManyField(Genero)
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True)
    likesRecibidos = models.ManyToManyField(User, related_name="likesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado like
    noLikesRecibidos = models.ManyToManyField(User, related_name="noLikesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado "no me gusta"

    def __str__(self):
        return self.usuario.username

    @property
    def numLikes(self):
        return self.likesRecibidos.all().count()
    @property
    def edad(self):
        return relativedelta(date.today(), self.fechaNacimiento).years

#Añadir ubicaciones para mejora del filtro de búsqueda
class Banda(models.Model):
    nombre = models.CharField(max_length=50)
    administrador = models.ForeignKey(Musico, on_delete = models.DO_NOTHING, related_name="bandasAdministradas") #Si desaparece el administrador, la banda puede seguir creada
    miembros = models.ManyToManyField(Musico, through='MiembroDe')
    def __str__(self):
        return self.nombre

class MiembroDe(models.Model):
    musico = models.ForeignKey(Musico, on_delete = models.CASCADE) #Si se borra el músico, esta relación se elimina, igual con la banda
    banda = models.ForeignKey(Banda, on_delete = models.CASCADE)
    fechaUnion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de unión")



#TimeStampedModel tiene campos de created y modified, que almacenan las horas de creación y modificación
#SoftDeletableModel en lugar de borrar una entrada de la tabla, le activa un campo llamado "is_removed"
class Chat(TimeStampedModel, SoftDeletableModel):
    participante1 = models.ForeignKey(Musico, verbose_name="Participante 1", on_delete=models.CASCADE, related_name="chats1")
    participante2 = models.ForeignKey(Musico, verbose_name="Participante 2", on_delete=models.CASCADE, related_name="chats2")

    def __str__(self):
        return "Chat de " + self.participante1.usuario.username + " con " + self.participante2.usuario.username


class Mensaje(TimeStampedModel, SoftDeletableModel):
    chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(Musico, verbose_name="Autor", on_delete=models.CASCADE, related_name="mensajes")
    cuerpo = models.TextField(verbose_name="Cuerpo del mensaje")
    #leido = models.BooleanField(verbose_name=_("Leido"), default=False)   #A tener en cuenta para posible mejora del chat, "doble check azul"

    def __str__(self):
        return self.autor.usuario.username + "(" + self.created + ") - '" + self.cuerpo + "'"

class Invitacion(TimeStampedModel):
    emisor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesEnviadas")
    receptor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesRecibidas")
    estado = models.BooleanField(default=False)
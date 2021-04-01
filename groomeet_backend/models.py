from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.db.models import Q
from typing import Optional, Any

# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

#Añadir ubicaciones para mejora del filtro de búsqueda
class Musico(AbstractUser):
    instrumentos = models.ManyToManyField(Instrumento)
    generos = models.ManyToManyField(Genero)
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True)
    def __str__(self):
        return self.username

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

class Match(models.Model):
    musico1 = models.ForeignKey(Musico, on_delete = models.CASCADE, related_name="matches1")
    musico2 = models.ForeignKey(Musico, on_delete = models.CASCADE, related_name="matches2")
    like1 = models.BooleanField(default=True)
    like2 = models.BooleanField(default=False)

#TimeStampedModel tiene campos de created y modified, que almacenan las horas de creación y modificación
#SoftDeletableModel en lugar de borrar una entrada de la tabla, le activa un campo llamado "is_removed"
class Chat(TimeStampedModel, SoftDeletableModel):
    participante1 = models.ForeignKey(Musico, verbose_name="Participante 1", on_delete=models.CASCADE, related_name="chats1")
    participante2 = models.ForeignKey(Musico, verbose_name="Participante 2", on_delete=models.CASCADE, related_name="chats2")

    def __str__(self):
        return "Chat de " + self.participante1.username + " con " + self.participante2.username

    @staticmethod
    def dialog_exists(u1: AbstractBaseUser, u2: AbstractBaseUser) -> Optional[Any]:
        return Chat.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        res = Chat.dialog_exists(u1, u2)
        if not res:
            Chat.objects.create(user1=u1, user2=u2)

    @staticmethod
    def chat_usuario(user: AbstractBaseUser):
        return Chat.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user1__pk', 'user2__pk')


class Mensaje(TimeStampedModel, SoftDeletableModel):
    chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(Musico, verbose_name="Autor", on_delete=models.CASCADE, related_name="mensajes")
    cuerpo = models.TextField(verbose_name="Cuerpo del mensaje")
    #leido = models.BooleanField(verbose_name=_("Leido"), default=False)   #A tener en cuenta para posible mejora del chat, "doble check azul"

    def __str__(self):
        return self.autor.username + "(" + self.created + ") - '" + self.cuerpo + "'"

class Invitacion(TimeStampedModel):
    emisor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesEnviadas")
    receptor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesRecibidas")
    estado = models.BooleanField(default=False)
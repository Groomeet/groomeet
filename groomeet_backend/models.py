from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel, SoftDeletableModel
from dateutil.relativedelta import relativedelta
from enum import Enum
import datetime


# Create your models here.

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    familia = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.nombre

#Método auxiliar para guardar la imagen como la id del usuario seguida de un punto
def rename_avatar_image(instance, filename):
        filesplits = filename.split('.')
        return 'media/images/avatars/%s.%s' % (instance.usuario.id, filesplits[-1])

class Chat(models.Model):
    nombre = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.nombre

#Añadir ubicaciones para mejora del filtro de búsqueda
class Musico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    instrumentos = models.ManyToManyField(Instrumento)
    generos = models.ManyToManyField(Genero,verbose_name="Géneros")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True)
    descripcion = models.TextField(verbose_name="Descripción")
    enlaceVideo = models.URLField(verbose_name="Enlace de vídeo", blank=True)
    avatar = models.ImageField(upload_to=rename_avatar_image, blank=True, null=True)
    chat = models.ManyToManyField(Chat, blank=True)
    #Sección de likes de Músico a Músico
    likesRecibidos = models.ManyToManyField(User, related_name="likesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado like
    noLikesRecibidos = models.ManyToManyField(User, related_name="noLikesDados", blank=True) #Tabla que relaciona con los usuarios que te han dado "no me gusta"
    #Sección de likes de Músico a Banda
    likesRecibidosBanda = models.ManyToManyField('Banda', related_name="likesDadosMusico", blank=True)
    noLikesRecibidosBanda = models.ManyToManyField('Banda', related_name="noLikesDadosMusico", blank=True)
    isGold = models.BooleanField(default=False)
    isSilver = models.BooleanField(default=False)
    isBoosted = models.BooleanField(default=False)
    superLikes = models.IntegerField(default=0)
    likesDisponibles = models.IntegerField(default=10)
    ultimaRenovacionLikes = models.DateField(default=datetime.date.today)
    ultimoUsuarioInteraccion = models.ManyToManyField(User, related_name="ultimoUsuarioInteraccion", blank=True)

    def __str__(self):
        return self.usuario.username

    @property
    def numLikes(self):
        return self.likesRecibidos.all().count()

    # @property
    # def edad(self):
    #     return relativedelta(date.today(), self.fechaNacimiento).years

#Método auxiliar para guardar la imagen como la id de la banda seguida de un punto
def rename_image_banda(instance, filename):
        filesplits = filename.split('.')
        return 'media/images/bandas/%s.%s' % (instance.id, filesplits[-1])

#Añadir ubicaciones para mejora del filtro de búsqueda
class Banda(models.Model):
    nombre = models.CharField(max_length=50)
    administrador = models.ForeignKey(Musico, on_delete = models.DO_NOTHING, related_name="bandasAdministradas") #Si desaparece el administrador, la banda puede seguir creada
    miembros = models.ManyToManyField(Musico, through='MiembroDe', blank=True)
    generos = models.ManyToManyField(Genero, blank=True)
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    descripcion = models.TextField(verbose_name="Descripción")
    enlaceVideo = models.URLField(verbose_name="Enlace de vídeo", blank=True)
    imagen = models.ImageField(verbose_name="Imagen de la banda",upload_to=rename_image_banda, blank=True, null=True)
    #Sección de likes de Banda a Músico
    likesRecibidosMusico = models.ManyToManyField(User, related_name="likesDadosBanda", blank=True)
    noLikesRecibidosMusico = models.ManyToManyField(User, related_name="noLikesDadosBanda", blank=True)
    #Sección de likes de Banda a Banda
    likesRecibidosBanda = models.ManyToManyField('Banda', related_name="likesDadosBanda", blank=True)
    noLikesRecibidosBanda = models.ManyToManyField('Banda', related_name="noLikesDadosBanda", blank=True)

    def __str__(self):
        return self.nombre

class MiembroNoRegistrado(models.Model):
    banda = models.ForeignKey(Banda, on_delete = models.CASCADE, related_name="miembrosNoRegistrados")
    nombre = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=500)
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    #foto?

    def __str__(self):
        return self.nombre

class MiembroDe(models.Model):
    musico = models.ForeignKey(Musico, on_delete = models.CASCADE) #Si se borra el músico, esta relación se elimina, igual con la banda
    banda = models.ForeignKey(Banda, on_delete = models.CASCADE)
    fechaUnion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de unión")



#TimeStampedModel tiene campos de created y modified, que almacenan las horas de creación y modificación
#SoftDeletableModel en lugar de borrar una entrada de la tabla, le activa un campo llamado "is_removed"
# class Chat(TimeStampedModel, SoftDeletableModel):
#     participante1 = models.ForeignKey(Musico, verbose_name="Participante 1", on_delete=models.CASCADE, related_name="chats1")
#     participante2 = models.ForeignKey(Musico, verbose_name="Participante 2", on_delete=models.CASCADE, related_name="chats2")

#     def __str__(self):
#         return "Chat de " + self.participante1.usuario.username + " con " + self.participante2.usuario.username


# class Mensaje(TimeStampedModel, SoftDeletableModel):
#     chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.CASCADE, related_name="mensajes")
#     autor = models.ForeignKey(Musico, verbose_name="Autor", on_delete=models.CASCADE, related_name="mensajes")
#     cuerpo = models.TextField(verbose_name="Cuerpo del mensaje")
#     #leido = models.BooleanField(verbose_name=_("Leido"), default=False)   #A tener en cuenta para posible mejora del chat, "doble check azul"

#     def __str__(self):
#         return self.autor.usuario.username + "(" + self.created + ") - '" + self.cuerpo + "'"

#Estado de las invitaciones a una banda
class EstadoInvitacion(Enum):
    Rechazada = "Rechazada"
    Pendiente = "Pendiente"
    Aceptada = "Aceptada"

class Invitacion(TimeStampedModel):
    emisor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesEnviadas")
    receptor = models.ForeignKey(Musico, on_delete=models.CASCADE, related_name="invitacionesRecibidas")
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=40,
        choices=[(estado, estado.value) for estado in EstadoInvitacion]
    )

class Producto(models.Model):
    producto = models.CharField(max_length=100, null= False)
    precio = models.DecimalField(max_digits=5 ,decimal_places= 2)

    def __str__(self):
        return self.producto

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    id = models.CharField(primary_key= True, max_length=100)
    estado = models.CharField(max_length=100)
    codigo_estado = models.CharField(max_length=100)
    producto = models.ForeignKey(to=Producto, on_delete= models.SET_NULL, null = True)
    total_de_la_compra = models.DecimalField(max_digits=5 ,decimal_places= 2)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    correo_cliente = models.EmailField(max_length=100)
    direccion_cliente = models.CharField(max_length=100)
    fecha_compra = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.nombre_cliente


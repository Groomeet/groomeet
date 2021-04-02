from django.contrib.auth.models import User
from django.db.models import base
from django.http import request
from django.contrib.messages.storage.fallback import FallbackStorage
from groomeet_backend.models import Musico,Instrumento, Genero
from groomeet_backend.likes import postLikeMusicoMusico, postNoLikeMusicoMusico
from django.test import RequestFactory, TestCase

# Create your tests here.
class LikesTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

        #Musico0 
        flauta = Instrumento.objects.create(nombre ="Flauta", familia ="Viento")
        rock = Genero.objects.create(nombre= "Rock")
        user = User.objects.create_user(username= "musico0",password="Probando0",email="musico0@gmail.com")
        musico0 = Musico.objects.create(usuario= user,fechaNacimiento="2001-09-12")
        musico0.instrumentos.add(flauta)
        musico0.generos.add(rock)

        #Musico1 
        bateria = Instrumento.objects.create(nombre ="Batería", familia ="Percusión")
        metal = Genero.objects.create(nombre= "Heavy Metal")
        user1 = User.objects.create_user(username= "musico1",password="Probando1",email="musico1@gmail.com")
        musico1 = Musico.objects.create(usuario= user1,fechaNacimiento="1998-12-12")
        musico1.instrumentos.add(bateria)
        musico1.generos.add(metal)
        musico1.generos.add(rock)

    def testGetUserById(self):
        user = User.objects.get(username="musico0")
        self.assertEqual(user.username,"musico0")

    def testLikeMusicoMusico(self):
        user0= User.objects.get(username="musico0")

        request = self.factory.get("/listado")
        request.user = user0

        user1= User.objects.get(username="musico1")
        musico1 = Musico.objects.get(usuario = user1)
        postLikeMusicoMusico(request, musico1.id)
        self.assertEqual(musico1.numLikes,1)

    def testNoLikeMusicoMusico(self):
        user0= User.objects.get(username="musico0")

        request = self.factory.get("/listado")
        request.user = user0

        user1= User.objects.get(username="musico1")
        musico1 = Musico.objects.get(usuario = user1)
        postNoLikeMusicoMusico(request, musico1.id)
        self.assertEqual(musico1.noLikesRecibidos.all().count(),1)

    def testMatchMusicoMusico(self):
        user0= User.objects.get(username="musico0")
        user1= User.objects.get(username="musico1")
        musico0 = Musico.objects.get(usuario = user0)
        musico1 = Musico.objects.get(usuario = user1)

        request = self.factory.get("/listado")
        request.user = user0

        postLikeMusicoMusico(request, musico1.id)
        request.user = user1
        request.session = {}
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        postLikeMusicoMusico(request, musico0.id)
        self.assertEqual(musico0.numLikes,1)
        self.assertEqual(musico1.numLikes,1)

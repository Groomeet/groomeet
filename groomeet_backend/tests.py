from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from groomeet_backend.models import Musico,Instrumento, Genero, Banda
from groomeet_backend.likes import postLikeBandaBanda, postLikeBandaMusico, postLikeMusicoBanda, postLikeMusicoMusico, postNoLikeBandaBanda, postNoLikeBandaMusico, postNoLikeMusicoBanda, postNoLikeMusicoMusico
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

        #Musico2
        guitarra = Instrumento.objects.create(nombre ="Guitarra", familia ="Cuerda")
        pop = Genero.objects.create(nombre= "Pop")
        user2 = User.objects.create_user(username= "musico2",password="Probando2",email="musico2@gmail.com")
        musico2 = Musico.objects.create(usuario= user2,fechaNacimiento="1997-09-15")
        musico2.instrumentos.add(guitarra)
        musico2.generos.add(pop)
        musico2.generos.add(rock)

        #Musico3
        bajo = Instrumento.objects.create(nombre ="Bajo", familia ="Cuerda")
        user3 = User.objects.create_user(username= "musico3",password="Probando3",email="musico3@gmail.com")
        musico3 = Musico.objects.create(usuario= user3,fechaNacimiento="2005-03-08")
        musico3.instrumentos.add(guitarra)
        musico3.instrumentos.add(bajo)
        musico3.generos.add(pop)

        #Banda0 Formada por: musico1
        banda1 = Banda.objects.create(nombre= "Banda1",administrador=musico1)
        banda1.generos.add(rock)
        banda1.generos.add(metal)
        banda1.instrumentos.add(bateria)
        banda1.miembros.add(musico1)
        
        #Banda1 Formada por: musico2 y musico3
        banda2 = Banda.objects.create(nombre= "Banda2",administrador=musico2)
        banda2.generos.add(rock)
        banda2.generos.add(pop)
        banda2.instrumentos.add(guitarra)
        banda2.instrumentos.add(bajo)
        banda2.instrumentos.add(bateria)
        banda2.miembros.add(musico2)
        banda2.miembros.add(musico3)
        

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

    def testLikeMusicoBanda(self):
        user0= User.objects.get(username="musico0")
        
        banda1 = Banda.objects.get(nombre="Banda1")

        request = self.factory.get("/listadoBandas")
        request.user = user0
        postLikeMusicoBanda(request,banda1.id)
        self.assertEqual(banda1.likesRecibidosMusico.all().count(),1)
        self.assertEqual(banda1.likesRecibidosBanda.all().count(),0)

    def testNoLikeMusicoBanda(self):
        user0= User.objects.get(username="musico0")
        
        banda1 = Banda.objects.get(nombre="Banda1")

        request = self.factory.get("/listadoBandas")
        request.user = user0
        postNoLikeMusicoBanda(request,banda1.id)
        self.assertEqual(banda1.noLikesRecibidosMusico.all().count(),1)
        self.assertEqual(banda1.noLikesRecibidosBanda.all().count(),0)

    def testMatchMusicoBanda(self):
        user0= User.objects.get(username="musico0")
        musico0 = Musico.objects.get(usuario = user0)

        user1=User.objects.get(username="musico1") 
        banda1 = Banda.objects.get(nombre="Banda1")

        request = self.factory.get("/listadoBandas")
        request.user = user0

        postLikeMusicoBanda(request,banda1.id)

        request = self.factory.get("/listadoBandasMusicos/"+str(banda1.id))
        request.user = user1
        request.session = {}
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        postLikeBandaMusico(request, banda1.id, musico0.id)
        self.assertEqual(musico0.likesRecibidosBanda.all().count(),1)
        self.assertEqual(banda1.likesRecibidosMusico.all().count(),1)

    def testLikeBandaMusico(self):
        user0= User.objects.get(username="musico0")
        musico0 = Musico.objects.get(usuario = user0)
        banda1 = Banda.objects.get(nombre="Banda1")

        request = self.factory.get("/listadoBandasMusicos/"+str(banda1.id))
        user1= User.objects.get(username="musico1")

        request.user = user1
        postLikeBandaMusico(request,banda1.id,musico0.id)
        self.assertEqual(musico0.likesRecibidosBanda.all().count(),1)

    def testNoLikeBandaMusico(self):
        user0= User.objects.get(username="musico0")
        musico0 = Musico.objects.get(usuario = user0)
        banda1 = Banda.objects.get(nombre="Banda1")

        request = self.factory.get("/listadoBandasMusicos/"+str(banda1.id))
        user1= User.objects.get(username="musico1")

        request.user = user1
        postNoLikeBandaMusico(request,banda1.id,musico0.id)
        self.assertEqual(musico0.noLikesRecibidosBanda.all().count(),1)
    
    def testLikeBandaBanda(self):
        banda1 = Banda.objects.get(nombre="Banda1")
        banda2 = Banda.objects.get(nombre="Banda2")
        request = self.factory.get("/buscarBandas/"+str(banda1.id))
        user1= User.objects.get(username="musico1")

        request.user = user1
        postLikeBandaBanda(request,banda1.id,banda2.id)
        self.assertEqual(banda2.likesRecibidosBanda.all().count(),1)

    def testNoLikeBandaBanda(self):        
        banda1 = Banda.objects.get(nombre="Banda1")
        banda2 = Banda.objects.get(nombre="Banda2")
        request = self.factory.get("/buscarBandas/"+str(banda1.id))
        user1= User.objects.get(username="musico1")

        request.user = user1
        postNoLikeBandaBanda(request,banda1.id,banda2.id)
        self.assertEqual(banda2.noLikesRecibidosBanda.all().count(),1)

    def testMatchBandaBanda(self):
        banda1 = Banda.objects.get(nombre="Banda1")
        banda2 = Banda.objects.get(nombre="Banda2")
        request = self.factory.get("/buscarBandas/"+str(banda1.id))
        user1= User.objects.get(username="musico1")

        request.user = user1
        postLikeBandaBanda(request,banda1.id,banda2.id)
        request = self.factory.get("/buscarBandas/"+str(banda2.id))
        user2= User.objects.get(username="musico2")
        request.user = user2
        request.session = {}
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        postLikeBandaBanda(request,banda2.id,banda1.id)
        self.assertEqual(banda1.likesRecibidosBanda.all().count(),1)
        self.assertEqual(banda2.likesRecibidosBanda.all().count(),1)
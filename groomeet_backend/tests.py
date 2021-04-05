from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from groomeet_backend.models import Musico,Instrumento, Genero, Banda
from groomeet_backend.likes import postLikeBandaBanda, postLikeBandaMusico, postLikeMusicoBanda, postLikeMusicoMusico, postNoLikeBandaBanda, postNoLikeBandaMusico, postNoLikeMusicoBanda, postNoLikeMusicoMusico
from django.test import RequestFactory, TestCase

# Create your tests here.

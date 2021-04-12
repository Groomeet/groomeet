"""groomeet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from groomeet_backend import views, likes, bandas, musicos
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('',views.musico, name='index'),
    path('signUp/',musicos.signUpMusico),
    path('updateProfile/',musicos.updateProfileMusico),
    path('buscarBandas',views.musico, name='index'),
    path('buscarIntegrantes/<int:pkBanda>',views.banda, name='index'),
    path('colabora/<int:pkBanda>',views.banda, name='index'),
    path('getMusico', views.getMusico, name="musico"),
    path('getBanda', views.getBanda, name="banda"),
    path('listadoBandas/',views.listadoBandas),
    path('listadoBandasMusicos/<int:pkBanda>',views.listadoBandasMusicos),
    path('buscarBandas/<int:pkBanda>',views.listadoBandasBandas),
    path("like/<int:pk>", likes.postLikeMusicoMusico, name="like"),
    path("noLike/<int:pk>", likes.postNoLikeMusicoMusico, name="noLike"),
    path("likeMusicoBanda/<int:pk>", likes.postLikeMusicoBanda, name="likeMusicoBanda"),
    path("noLikeMusicoBanda/<int:pk>", likes.postNoLikeMusicoBanda, name="noLikeMusicoBanda"),
    path("likeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postLikeBandaMusico, name="likeBandaMusico"),
    path("noLikeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postNoLikeBandaMusico, name="noLikeBandaMusico"),
    path("likeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postLikeBandaBanda, name="likeBandaBanda"),
    path("noLikeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postNoLikeBandaBanda, name="noLikeBandaBanda"),
    path('createBanda/',bandas.bandaCreate),
    path('createMiembroNoRegistrado/<int:pk>',bandas.miembroNoRegistradoCreate),
    path('misBandas/',views.listadoMisBandas),
    path('updateBanda/<int:id>', bandas.bandaUpdate, name='updateBanda'),
    path('deleteBanda/<int:id>', bandas.bandaDelete, name='deleteBanda'),
    path('invitacionBanda/<int:banda_id>/', bandas.enviarInvitacionBanda),
    path('aceptarInvitacion/<int:invitacion_id>/', bandas.aceptarInvitacionBanda),
    path('rechazarInvitacion/<int:invitacion_id>/',bandas.rechazarInvitacionBanda),
    path('misInvitaciones/',views.listadoMisInvitaciones),
    path('chat/', include('groomeet_backend.urls')),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room')

]

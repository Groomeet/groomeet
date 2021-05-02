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
from groomeet_backend import views, likes, bandas, pagos, musicos
from django.contrib.auth import views as auth_views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
#from groomeet_backend.views import error_404,error_500
from django.views.static import serve

handler404 = 'groomeet_backend.views.handler404'
handler500 = 'groomeet_backend.views.handler404'
handler503 = 'groomeet_backend.views.handler404'

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
    path('getMusico/<int:pkBanda>', views.getMusico2, name="musico"),
    path('getBanda', views.getBanda, name="banda"),
    path('getBanda/<int:pkBanda>', views.getBanda2, name="musico"),
    path("like/<int:pk>", likes.postLikeMusicoMusico, name="like"),
    path("superLike/<int:pk>", likes.postSuperLikeMusicoMusico, name="superlikeMusicoMusico"),
    path("noLike/<int:pk>", likes.postNoLikeMusicoMusico, name="noLike"),
    path("likeMusicoBanda/<int:pk>", likes.postLikeMusicoBanda, name="likeMusicoBanda"),
    path("superLikeMusicoBanda/<int:pk>", likes.postSuperLikeMusicoBanda, name="superLikeMusicoBanda"),
    path("noLikeMusicoBanda/<int:pk>", likes.postNoLikeMusicoBanda, name="noLikeMusicoBanda"),
    path("likeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postLikeBandaMusico, name="likeBandaMusico"),
    path("superLikeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postSuperLikeBandaMusico, name="superLikeBandaMusico"),
    path("noLikeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postNoLikeBandaMusico, name="noLikeBandaMusico"),
    path("likeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postLikeBandaBanda, name="likeBandaBanda"),
    path("superLikeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postSuperLikeBandaBanda, name="superLikeBandaBanda"),
    path("noLikeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postNoLikeBandaBanda, name="nolikeBandaBanda"),
    path("undoLikeMusicoMusico/<int:pk>", likes.postUndoLikeMusicoMusico, name="undoLikeMusicoMusico"),
    path("undoLikeMusicoBanda/<int:pk>", likes.postUndoLikeMusicoBanda, name="undoLikeMusicoBanda"),
    path("undoLikeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postUndoLikeBandaMusico, name="undoLikeBandaMusico"),
    path("undoLikeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postUndoLikeBandaBanda, name="undoLikeBandaBanda"),
    path("undoDislikeMusicoMusico/<int:pk>", likes.postUndoDislikeMusicoMusico, name="undoDislikeMusicoMusico"),
    path("undoDislikeMusicoBanda/<int:pk>", likes.postUndoDislikeMusicoBanda, name="undoDislikeMusicoBanda"),
    path("undoDislikeBandaMusico/<int:pkBanda>/<int:pkMusico>", likes.postUndoDislikeBandaMusico, name="undoDislikeBandaMusico"),
    path("undoDislikeBandaBanda/<int:pkEmisor>/<int:pkReceptor>", likes.postUndoDislikeBandaBanda, name="undoDislikeBandaBanda"),
    path('createBanda/',bandas.bandaCreate),
    path('createMiembroNoRegistrado/<int:pk>',bandas.miembroNoRegistradoCreate),
    path('misBandas/',views.listadoMisBandas),
    path('showBanda/<int:id>/',views.showBanda),
    path('updateBanda/<int:id>', bandas.bandaUpdate, name='updateBanda'),
    path('deleteBanda/<int:id>', bandas.bandaDelete, name='deleteBanda'),
    path('invitacionBanda/<int:banda_id>/', bandas.enviarInvitacionBanda),
    path('showInvitacion/<int:id>', bandas.showInvitacion),
    path('aceptarInvitacion/<int:invitacion_id>/', bandas.aceptarInvitacionBanda),
    path('rechazarInvitacion/<int:invitacion_id>/',bandas.rechazarInvitacionBanda),
    path('eliminarMiembro/<int:pkBanda>/<int:pkMusico>',bandas.eliminarMiembroBanda),
    path('eliminarMiembroNoRegistrado/<int:pkBanda>/<int:pkMiembro>',bandas.eliminarMiembroNoRegistrado),
    path('misInvitaciones/',views.listadoMisInvitaciones),
    path('pago/<int:id>', pagos.pago, name= 'pago'),
    path('listadoProductos/', pagos.listadoProductos, name= 'listadoProductos'),
    path('comprarProducto/<int:pk>', pagos.comprarProducto, name= 'comprarProducto'),
    path('chat/', include('groomeet_backend.urls')),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
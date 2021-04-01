from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from groomeet_backend import views
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf.urls import url, include

from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser

from typing import List
from django_private_chat2 import urls as django_private_chat2_urls

UserModel = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context['object_list']

        data = [{
            "username": user.get_username(),
            "pk": str(user.pk)
        } for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)

urlpatterns = [
    url('chat/', include('django_private_chat2.urls', namespace='django_private_chat2')),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('', login_required(TemplateView.as_view(template_name='base.html')), name='home'),
]


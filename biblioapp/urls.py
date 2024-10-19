from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("prestar/<int:libro_id>", views.prestar, name="prestar"),
    path("prestado/<int:libro_id>", views.prestado, name="prestado"),
    path("usuario/salir", views.salir, name="salir"),
    path("usuario/ingresar", views.ingresar, name="ingresar"),
    path("usuario/registrarse", views.registrarse, name="registrarse"),
    path("usuario/", views.perfil, name="perfil")
]
from django.db import models

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage()

class Libro(models.Model):
    autor = models.CharField(max_length=128)
    nombre = models.CharField(max_length=128)
    portada = models.URLField()
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} de {self.autor}"


class Prestamo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    libro = models.ForeignKey(Libro, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Prestamo de {self.usuario} de {self.libro}"

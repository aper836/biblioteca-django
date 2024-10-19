from django.contrib import admin
from .models import Libro, Prestamo

# Register your models here.

admin.site.register(Libro)
admin.site.register(Prestamo)

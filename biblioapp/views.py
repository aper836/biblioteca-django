from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from .models import Libro, Prestamo


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.models import User


def index(request: HttpRequest):
    if request.method == "POST":
        
        if not request.user.is_authenticated:
            return redirect("index")
        
        usuario = request.user
        libro_id = request.POST["libro_id"]
        libro = Libro.objects.get(pk=libro_id)

        conteo = Prestamo.objects.filter(libro=libro).count()

        if conteo > libro.cantidad:
            return HttpResponse("Excedido")

        prestados = Prestamo.objects.filter(usuario=usuario)

        if prestados.count() > 3:
            return HttpResponse("Excedido el numero de prestamos")

        tieneEste = prestados.filter(libro=libro)
        if tieneEste.count() == 1:
            return HttpResponse("Ya presto este libro")

        Prestamo.objects.create(usuario=usuario, libro=libro)

        return redirect("index")
    
    libros_obtenidos = []
    if request.user.is_authenticated:
        prestados = Prestamo.objects.filter(usuario=request.user).values_list('libro', flat=True)
        libros_obtenidos = list(prestados)
    
    print(libros_obtenidos)
    libros = Libro.objects.all()

    context = {
        "libros": libros,
        "user" : request.user,
        "curpath" : request.path,
        "obtenidos" : libros_obtenidos
    }

    return render(request, "index.html", context)


def libro_detail(request, libro_id):
    
    libro = Libro.objects.get(pk=libro_id)
    if libro is None:
        return Http404("No existe el libro")
    
    return render(request, "libro_detail.html", {"libro" : libro})

@login_required
def prestado(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, "prestado.html", {'libro' : libro})

@login_required
def prestar(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    
    return HttpResponseRedirect(f"/prestado/{libro_id}")

@login_required
def salir(request):
    logout(request)

    return HttpResponseRedirect(request.GET.get('next'))

def registrarse(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["password"]
        password = request.POST["password"]

        existe = User.objects.filter(username=username).count()

        if existe > 0:
            return HttpResponse("El usuario ya existe")

        User.objects.create(request, username=username, email=email, password=password)

        return redirect("index")

    return render(request, "registrarse.html")


def ingresar(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            print("error")


        return redirect("index")

    return render(request, "ingresarForm.html")



@login_required
def perfil(request):
    librosQuery = Prestamo.objects.filter(usuario=request.user).values_list('libro', flat=True)

    libros = []
    for i in librosQuery.iterator():
        libros.append(Libro.objects.get(pk=i))

    return render(request, "perfil.html", { "libros" : libros })

from django.shortcuts import render, get_object_or_404, redirect
from apps.posts.models import Articulo, Comentario, Categoria
from .forms import ArticuloForm, ComentarioForm
from django.contrib.auth.decorators import login_required

def index(request):
    articulos = Articulo.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        articulos = articulos.filter(categoria=categoria)

    antiguedad = request.GET.get('antiguedad')
    if antiguedad == 'asc':
        articulos = articulos.order_by('fecha_publicacion')
    elif antiguedad == 'desc':
        articulos = articulos.order_by('-fecha_publicacion')

    return render(request, 'blog/index.html', {'articulos': articulos})

def categorias(request):
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        articulos = Articulo.objects.filter(categoria=categoria)
    else:
        articulos = Articulo.objects.all()

    return render(request, 'blog/categorias.html', {'categorias': categorias, 'articulos': articulos})

def contacto(request):
    return render(request, 'blog/contacto.html')

def agregar_comentario(request, articulo_id):
    return render(request, 'blog/agregar_comentario.html')

def registro_usuario(request):
    # Lógica para el registro de usuarios
    return render(request, 'blog/registro_usuario.html')

def perfil_usuario(request):
    # Lógica para la página de perfil de usuario
    return render(request, 'blog/perfil_usuario.html')

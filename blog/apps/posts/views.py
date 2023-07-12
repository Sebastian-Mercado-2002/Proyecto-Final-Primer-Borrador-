from django.shortcuts import render, get_object_or_404, redirect
from .models import Articulo, Comentario, Categoria
from .forms import ArticuloForm, ComentarioForm
from django.contrib.auth.decorators import login_required

@login_required
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.autor = request.user
            articulo.save()
            return redirect('posts:articulo', articulo_id=articulo.id)
    else:
        form = ArticuloForm()
    
    return render(request, 'crear_articulo.html', {'form': form})

@login_required
def editar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    
    if articulo.autor != request.user:
        return redirect('posts:articulo', articulo_id=articulo.id)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('posts:articulo', articulo_id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)
    
    return render(request, 'editar_articulo.html', {'form': form, 'articulo': articulo})

@login_required
def eliminar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    
    if articulo.autor != request.user:
        return redirect('posts:articulo', articulo_id=articulo.id)
    
    articulo.delete()
    
    return redirect('posts:index')

def articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    comentarios = Comentario.objects.filter(articulo=articulo)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.save()
            return redirect('posts:articulo', articulo_id=articulo_id)
    else:
        form = ComentarioForm()

    return render(request, 'articulo.html', {'articulo': articulo, 'comentarios': comentarios, 'form': form})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    if comentario.autor != request.user:
        return redirect('posts:articulo', articulo_id=comentario.articulo.id)
    
    articulo_id = comentario.articulo.id

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('posts:articulo', articulo_id=articulo_id)
    else:
        form = ComentarioForm(instance=comentario)
    
    return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario, 'articulo_id': articulo_id})

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    if comentario.autor != request.user:
        return redirect('posts:articulo', articulo_id=comentario.articulo.id)
    
    articulo_id = comentario.articulo.id
    
    comentario.delete()
    
    return redirect('posts:articulo', articulo_id=articulo_id)

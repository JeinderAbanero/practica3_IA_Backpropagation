from django.shortcuts import render
from .models import Usuario, Cuenta
from .mlp_model import classifier
from datetime import datetime

def get_account_age(fecha_creacion):
    """
    Calcula la antigüedad de la cuenta en años.
    Maneja tanto fechas completas como solo años.
    """
    try:
        if '-' in str(fecha_creacion):
            # Si es una fecha completa (YYYY-MM-DD)
            fecha = datetime.strptime(str(fecha_creacion), '%Y-%m-%d')
            return datetime.now().year - fecha.year
        else:
            # Si es solo el año
            return datetime.now().year - int(fecha_creacion)
    except (ValueError, TypeError):
        return 0

def index(request):
    usuarios = Usuario.objects.select_related('cuenta').all()
    for usuario in usuarios:
        if hasattr(usuario, 'cuenta'):
            antiguedad = get_account_age(usuario.cuenta.fecha_creacion)
            usuario.antiguedad = antiguedad  # Agregamos la antigüedad al objeto usuario
            features = [
                usuario.cuenta.promedio_hashtags_por_publicacion,
                usuario.cuenta.promedio_publicaciones_por_dia,
                usuario.cuenta.promedio_comentarios_por_dia,
                usuario.cuenta.seguidos,
                usuario.cuenta.seguidores,
                antiguedad
            ]
            resultado = classifier.predict(features)
            usuario.clasificacion = resultado["clasificacion"]
            usuario.probabilidad = resultado["probabilidad"]
    
    return render(request, 'index.html', {'usuarios': usuarios})

def juzgar(request, username):
    usuario = Usuario.objects.select_related('cuenta').get(username=username)
    cuenta = usuario.cuenta
    publicaciones = cuenta.publicaciones.prefetch_related('comentarios').all()
    antiguedad = get_account_age(cuenta.fecha_creacion)
    
    features = [
        cuenta.promedio_hashtags_por_publicacion,
        cuenta.promedio_publicaciones_por_dia,
        cuenta.promedio_comentarios_por_dia,
        cuenta.seguidos,
        cuenta.seguidores,
        antiguedad
    ]
    
    resultado = classifier.predict(features)
    
    return render(request, 'juzgar.html', {
        'usuario': usuario,
        'cuenta': cuenta,
        'publicaciones': publicaciones,
        'antiguedad': antiguedad,
        'clasificacion': resultado["clasificacion"],
        'probabilidad': resultado["probabilidad"]
    })

def evaluar_manual(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        hashtags = float(request.POST.get('hashtags'))
        posts = float(request.POST.get('posts'))
        comments = float(request.POST.get('comments'))
        following = int(request.POST.get('following'))
        followers = int(request.POST.get('followers'))
        age = float(request.POST.get('age'))

        # Crear el vector de características
        features = [hashtags, posts, comments, following, followers, age]
        
        # Obtener la predicción
        resultado = classifier.predict(features)
        
        # Renderizar el template con el resultado y las estadísticas
        return render(request, 'evaluar_manual.html', {
            'resultado': resultado,
            'hashtags': hashtags,
            'posts': posts,
            'comments': comments,
            'following': following,
            'followers': followers,
            'age': age
        })
    
    return render(request, 'evaluar_manual.html')

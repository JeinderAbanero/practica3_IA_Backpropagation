import json
import os
import sys
import django
import random
# Definir la ruta base del proyecto
# Definir la ruta base del proyecto

# Obtener la ruta del directorio actual (donde está cargar_usuarios.py)
current_dir = os.path.dirname(__file__)
ruta_archivo = os.path.join(current_dir, "usuarios.json")

# Configurar Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backpropagation.settings")
django.setup()


from django.core.management.base import BaseCommand
from backpropagation.models import Usuario, Cuenta, Publicacion, Comentario
from datetime import datetime

class Command(BaseCommand):
    help = 'Carga datos de usuarios desde un archivo JSON a la base de datos'

    def handle(self, *args, **kwargs):
        # Limpiar datos existentes
        self.stdout.write("Limpiando datos existentes...")
        Usuario.objects.all().delete()
        
        # Ruta al archivo JSON
        ruta_json = ruta_archivo

        # Leer el archivo JSON
        with open(ruta_json, "r", encoding="utf-8") as f:
            datos = json.load(f)

        if isinstance(datos, list):
            random.shuffle(datos)  # Mezclar los datos de forma aleatoria

        # Recorrer los usuarios en el JSON
        for dato_usuario in datos:
            # Crear el usuario
            usuario = Usuario.objects.create(
                username=dato_usuario["username"],
                first_name=dato_usuario["first_name"],
                last_name=dato_usuario["last_name"],
                email=dato_usuario["email"],
                password=dato_usuario["password"],
                etiqueta=dato_usuario["etiqueta"]  # Añadido campo etiqueta
            )
            self.stdout.write(f"Usuario {usuario.username} creado con etiqueta {usuario.etiqueta}")

            # Crear la cuenta asociada al usuario
            cuenta = Cuenta.objects.create(
                usuario=usuario,
                seguidores=dato_usuario["cuenta"]["seguidores"],
                seguidos=dato_usuario["cuenta"]["seguidos"],
                fecha_creacion=dato_usuario["cuenta"]["fecha_creacion"],
                promedio_hashtags_por_publicacion=dato_usuario["cuenta"]["promedio_hashtags_por_publicacion"],
                promedio_publicaciones_por_dia=dato_usuario["cuenta"]["promedio_publicaciones_por_dia"],
                promedio_comentarios_por_dia=dato_usuario["cuenta"]["promedio_comentarios_por_dia"],
            )

            # Crear las publicaciones asociadas a la cuenta
            for dato_publicacion in dato_usuario["publicaciones"]:
                publicacion = Publicacion.objects.create(
                    cuenta=cuenta,
                    titulo=dato_publicacion["titulo"],
                    texto=dato_publicacion["texto"],
                    fecha_publicacion=datetime.strptime(dato_publicacion["fecha_publicacion"], "%Y-%m-%d")
                )

                # Crear los comentarios asociados a la publicación
                for dato_comentario in dato_publicacion["comentarios"]:
                    Comentario.objects.create(
                        publicacion=publicacion,
                        usuario=dato_comentario["usuario"],
                        texto_comentario=dato_comentario["texto_comentario"],
                        fecha_comentario=datetime.strptime(dato_comentario["fecha_comentario"], "%Y-%m-%d")
                    )

        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente en la base de datos.'))
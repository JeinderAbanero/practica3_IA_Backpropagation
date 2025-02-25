from django.core.management.base import BaseCommand
from faker import Faker
import json
import random
from datetime import datetime, timedelta

fake = Faker()

def generar_usuarios(cantidad, etiqueta):
    usuarios = []
    for _ in range(cantidad):
        if etiqueta == "Spawn Bot":
            # Características de bot
            seguidores = random.randint(5, 101)  # Pocos seguidores
            seguidos = random.randint(800, 1501)  # Muchos seguidos
            antiguedad = random.randint(0, 2)  # Cuenta nueva
            hashtags = random.uniform(8, 16)  # Muchos hashtags
            posts = random.uniform(5, 10)  # Muchas publicaciones
            comentarios = random.uniform(20, 50)  # Muchos comentarios
        else:
            # Características de usuario normal
            seguidores = random.randint(400, 1001)  # Más seguidores
            seguidos = random.randint(50, 201)  # Menos seguidos
            antiguedad = random.randint(5, 15)  # Cuenta más antigua
            hashtags = random.uniform(1, 4)  # Menos hashtags
            posts = random.uniform(1, 3)  # Menos publicaciones
            comentarios = random.uniform(5, 15)  # Menos comentarios

        fecha_creacion = str(datetime.now().year - antiguedad)
        
        usuario = {
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "etiqueta": etiqueta,
            "cuenta": {
                "seguidores": seguidores,
                "seguidos": seguidos,
                "fecha_creacion": fecha_creacion,
                "promedio_hashtags_por_publicacion": round(hashtags, 2),
                "promedio_publicaciones_por_dia": round(posts, 2),
                "promedio_comentarios_por_dia": round(comentarios, 2)
            },
            "publicaciones": generar_publicaciones(random.randint(3, 10), hashtags)
        }
        usuarios.append(usuario)
    return usuarios

def generar_publicaciones(cantidad, promedio_hashtags):
    publicaciones = []
    for _ in range(cantidad):
        num_hashtags = round(random.gauss(promedio_hashtags, 1))
        num_hashtags = max(0, num_hashtags)  # Asegurar que no sea negativo
        
        hashtags = ' '.join([f"#{fake.word()}" for _ in range(num_hashtags)])
        fecha = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        
        publicacion = {
            "titulo": fake.sentence(),
            "texto": f"{fake.paragraph()} {hashtags}",
            "fecha_publicacion": fecha,
            "comentarios": generar_comentarios(random.randint(1, 5))
        }
        publicaciones.append(publicacion)
    return publicaciones

def generar_comentarios(cantidad):
    comentarios = []
    for _ in range(cantidad):
        fecha = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        comentario = {
            "usuario": fake.user_name(),
            "texto_comentario": fake.sentence(),
            "fecha_comentario": fecha
        }
        comentarios.append(comentario)
    return comentarios

def generar_data_json(usuarios):
    data = []
    for usuario in usuarios:
        cuenta = usuario["cuenta"]
        features = [
            cuenta["promedio_hashtags_por_publicacion"],
            cuenta["promedio_publicaciones_por_dia"],
            cuenta["promedio_comentarios_por_dia"],
            cuenta["seguidos"],
            cuenta["seguidores"],
            int(datetime.now().year) - int(cuenta["fecha_creacion"])
        ]
        label = 1 if usuario["etiqueta"] == "Spawn Bot" else 0
        data.append({"features": features, "label": label})
    return data

class Command(BaseCommand):
    help = 'Genera datos de usuarios para entrenamiento y prueba'

    def handle(self, *args, **kwargs):
        # Generar datos balanceados (50% bots, 50% normales)
        usuarios_bot = generar_usuarios(5, "Spawn Bot")
        usuarios_normal = generar_usuarios(5, "normal")
        usuarios = usuarios_bot + usuarios_normal
        
        # Guardar usuarios en JSON
        with open("backpropagation/management/commands/usuarios.json", "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)
            
        # Generar y guardar datos de entrenamiento
        data = generar_data_json(usuarios)
        with open("backpropagation/management/commands/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        self.stdout.write("JSON generado exitosamente: usuarios.json y data.json")
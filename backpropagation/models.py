from django.db import models

# Modelo Usuario
class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    etiqueta = models.CharField(max_length=20, default='normal')  # Añadido campo etiqueta

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.username


# Modelo Cuenta
class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta')
    seguidores = models.IntegerField(default=0)  # spawnbot (5, 101), normal (400, 1001) 
    seguidos = models.IntegerField(default=0)    # spawnbot (800, 1501), normal (50, 201)
    fecha_creacion = models.CharField(max_length=10, default='0')  # spawnbot(0, 2) años, normal (5, 15) años
    promedio_hashtags_por_publicacion = models.FloatField(default=0)  # spawnbot (8, 16), normal (1, 4)
    promedio_publicaciones_por_dia = models.FloatField(default=0)     # spawnbot (5, 10), normal (1, 3)
    promedio_comentarios_por_dia = models.FloatField(default=0)       # spawnbot (20, 50), normal (5, 15)

    class Meta:
        db_table = 'cuentas'

    def __str__(self):
        return f"Cuenta de {self.usuario.username}"


# Modelo Publicacion
class Publicacion(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='publicaciones')
    titulo = models.CharField(max_length=200)  # recuerda agregarle los hashtags para que coincida con el promedio (#)
    texto = models.TextField()
    fecha_publicacion = models.DateField()  # recuerda agregar varios para que coincidan con el dia 

    class Meta:
        db_table = 'publicaciones'

    def __str__(self):
        return f"{self.titulo} - {self.cuenta.usuario.username}"


# Modelo Comentario
class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.CharField(max_length=50)  # Username del comentarista
    texto_comentario = models.TextField()
    fecha_comentario = models.DateField()

    class Meta:
        db_table = 'comentarios'

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.publicacion.titulo}"

# Bot Detection System

Sistema de detección de bots en redes sociales utilizando una red neuronal MLP (Multi-Layer Perceptron).

## Características

- Detección de bots basada en patrones de comportamiento
- Interfaz web para evaluación manual de usuarios
- Modelo MLP entrenado con datos reales
- Visualización detallada de estadísticas de usuario
- Clasificación en tiempo real de usuarios

## Métricas Analizadas

El sistema analiza las siguientes características para determinar si un usuario es un bot:

- Promedio de hashtags por publicación
- Promedio de publicaciones por día
- Promedio de comentarios por día
- Número de seguidos
- Número de seguidores
- Antigüedad de la cuenta (en años)

## Requisitos

- Python 3.11+
- PostgreSQL
- Django 5.0+

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd backpropagation
```

2. Instalar dependencias requeridas:
```bash
pip install numpy
pip install Faker
pip install psycopg2
pip install -r requirements.txt
```

3. Configurar la base de datos PostgreSQL:
   - Crear una base de datos llamada 'bot_detection'
   - Configurar las credenciales en settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bot_detection',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Generar datos de entrenamiento:
```bash
python manage.py generarJsonDB
```

6. Entrenar el algoritmo:
```bash
python manage.py train_mlp
```

7. Cargar datos en la base de datos:
```bash
python manage.py cargar_dataDB
```

8. Iniciar el servidor:
```bash
python manage.py runserver
```

## Uso

1. Acceder a la interfaz web en `http://localhost:8000`
2. Ver la lista de usuarios y sus clasificaciones en la página principal
3. Usar "Evaluación Manual" para analizar estadísticas personalizadas
4. Ver detalles de usuario específico haciendo clic en su nombre

El sistema proporciona:
- Clasificación (Spawn Bot/Normal)
- Probabilidad de la clasificación
- Estadísticas detalladas del usuario
- Historial de publicaciones y comentarios

## Estructura del Proyecto

```
backpropagation/
├── backpropagation/        # Aplicación principal
│   ├── management/        # Comandos personalizados
│   │   └── commands/     # Comandos para carga de datos y entrenamiento
│   ├── migrations/       # Migraciones de la base de datos
│   ├── templates/       # Plantillas HTML
│   ├── mlp_model.py    # Implementación del modelo MLP
│   ├── models.py       # Modelos de Django
│   ├── views.py        # Vistas de Django
│   └── urls.py         # URLs de la aplicación
├── manage.py           # Script de gestión de Django
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Documentación
```

## Funcionamiento del Modelo

El sistema utiliza un perceptrón multicapa (MLP) con:
- 6 neuronas de entrada (una por cada métrica)
- 8 neuronas en la capa oculta
- 1 neurona de salida (probabilidad de ser bot)

La clasificación se realiza en tiempo real, analizando los patrones de comportamiento del usuario y comparándolos con los patrones aprendidos durante el entrenamiento.

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

# Bot Detection System

Sistema de detección de bots en redes sociales utilizando una red neuronal MLP (Multi-Layer Perceptron).

## Características

- Detección de bots basada en patrones de comportamiento
- Interfaz web para evaluación manual de usuarios
- Modelo MLP entrenado con datos reales
- API para integración con otros sistemas

## Métricas Analizadas

- Hashtags por publicación
- Publicaciones por día
- Comentarios por día
- Número de seguidos
- Número de seguidores
- Antigüedad de la cuenta

## Requisitos

- Python 3.8+
- Django 4.2+
- NumPy

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd backpropagation2
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:
```bash
python manage.py migrate
```

4. Entrenar el modelo:
```bash
python manage.py train_mlp
```

5. Iniciar el servidor:
```bash
python manage.py runserver
```

## Uso

1. Acceder a la interfaz web en `http://localhost:8000`
2. Usar la opción "Evaluación Manual" para analizar usuarios individuales
3. Los resultados mostrarán la clasificación (Bot/Normal) y la probabilidad

## Estructura del Proyecto

```
backpropagation2/
├── backpropagation/         # Aplicación principal
│   ├── management/         # Comandos personalizados
│   ├── migrations/         # Migraciones de la base de datos
│   ├── templates/         # Plantillas HTML
│   ├── mlp_model.py      # Implementación del modelo MLP
│   ├── views.py          # Vistas de Django
│   └── urls.py           # URLs de la aplicación
├── backpropagation2/       # Configuración del proyecto
└── manage.py              # Script de gestión de Django
```

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

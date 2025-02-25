import numpy as np
import json
import os

# Definir la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_archivo = os.path.join(BASE_DIR, "scripts", "data.json")

# Función para generar datos sintéticos
def generate_data(num_samples):
    X = []
    y = []

    for _ in range(num_samples):
        # Spawn Bot
        X.append([
            np.random.randint(5, 10),       # publicaciones_por_dia
            np.random.randint(8, 16),        # hashtags_por_publicacion
            np.random.randint(10, 101),      # seguidores
            np.random.randint(800, 1501),    # seguidos
            np.random.randint(20, 50),       # comentarios realizados por dia 
            np.random.uniform(0, 2)          # fecha_creacion_cuenta
        ])
        y.append(1)  # Etiqueta para Spawn Bot

        # Normal
        X.append([
            np.random.randint(1, 3),         # publicaciones_por_dia
            np.random.randint(1, 4),         # promedio hashtags_por_publicacion
            np.random.randint(400, 1001),    # seguidores
            np.random.randint(50, 201),      # seguidos
            np.random.randint(5, 15),        # promedio comentarios realizados por dia
            np.random.uniform(5, 10)         # fecha_creacion_cuenta
        ])
        y.append(0)  # Etiqueta para Normal

    return X, y

# Generar datos
num_samples = 100  # Número de ejemplos por categoría
X, y = generate_data(num_samples)

# Guardar en JSON
data = {"X": X, "y": y}
with open(ruta_archivo, "w") as file:
    json.dump(data, file, indent=4)
    #json.dump(data, file)

print(f"Archivo JSON generado con {2 * num_samples} ejemplos (Spawn Bot y Normal).")
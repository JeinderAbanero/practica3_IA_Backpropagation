from django.core.management.base import BaseCommand
import numpy as np
import json
import os
from backpropagation.mlp_model import MLPClassifier

class Command(BaseCommand):
    help = 'Entrena el modelo MLP con los datos de entrenamiento'

    def handle(self, *args, **kwargs):
        # Cargar datos
        current_dir = os.path.dirname(__file__)
        data_path = os.path.join(current_dir, 'data.json')
        
        with open(data_path, 'r') as f:
            data = json.load(f)
            
        # Convertir datos a numpy arrays
        X = []
        y = []
        for item in data:
            X.append(item['features'])
            y.append(item['label'])
            
        X = np.array(X, dtype=np.float64)
        y = np.array(y, dtype=np.float64).reshape(-1, 1)
        
        # Normalizar características
        mean = np.mean(X, axis=0)
        std = np.std(X, axis=0)
        X_norm = (X - mean) / (std + 1e-8)
        
        # Crear y entrenar modelo
        classifier = MLPClassifier()
        classifier.mlp.train(X_norm, y, epochs=20000, learning_rate=0.01)
        
        # Guardar pesos y parámetros de normalización
        classifier.save_weights(mean=mean, std=std)
        
        self.stdout.write(self.style.SUCCESS('Modelo entrenado y guardado exitosamente'))
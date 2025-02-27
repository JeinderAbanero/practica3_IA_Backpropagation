import numpy as np
import json
import os

class MLP:
    def __init__(self, input_size=6, hidden_size=8, output_size=1):
        """Inicializa el perceptrón multicapa"""
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Inicialización de pesos con valores pequeños aleatorios
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))

    def sigmoid(self, x):
        """Función de activación sigmoide"""
        return 1 / (1 + np.exp(-np.clip(x, -10, 10)))

    def sigmoid_derivative(self, x):
        """Derivada de la función sigmoide"""
        return x * (1 - x)

    def forward(self, X):
        """Propagación hacia adelante"""
        # Asegurar que X sea un array 2D
        if len(X.shape) == 1:
            X = X.reshape(1, -1)
            
        # Primera capa
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        
        # Segunda capa
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        
        return self.a2

    def backward(self, X, y, learning_rate=0.01):
        """Retropropagación del error"""
        m = X.shape[0]
        
        # Calcular gradientes
        dZ2 = self.a2 - y
        dW2 = np.dot(self.a1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        dZ1 = np.dot(dZ2, self.W2.T) * self.sigmoid_derivative(self.a1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # Actualizar pesos y sesgos
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    def train(self, X, y, epochs=10000, learning_rate=0.01, verbose=True):
        """Entrena el modelo con early stopping"""
        best_loss = float('inf')
        patience = 10
        patience_counter = 0
        best_weights = None
        
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Calcular pérdida
            loss = np.mean(np.square(y - output))
            
            if epoch % 1000 == 0 and verbose:
                print(f'Epoch {epoch}, Loss: {loss:.6f}')
            
            # Early stopping
            if loss < best_loss:
                best_loss = loss
                patience_counter = 0
                best_weights = {
                    'W1': self.W1.copy(),
                    'W2': self.W2.copy(),
                    'b1': self.b1.copy(),
                    'b2': self.b2.copy()
                }
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if verbose:
                        print(f'Early stopping en epoch {epoch}')
                    break
            
            # Backward pass
            self.backward(X, y, learning_rate)
        
        # Restaurar los mejores pesos
        if best_weights is not None:
            self.W1 = best_weights['W1']
            self.W2 = best_weights['W2']
            self.b1 = best_weights['b1']
            self.b2 = best_weights['b2']

class MLPClassifier:
    def __init__(self):
        """Inicializa el clasificador"""
        self.mlp = MLP()
        self.mean = None
        self.std = None
        self.weights_file = os.path.join(os.path.dirname(__file__), 'mlp_weights.json')
        self._load_weights()

    def _load_weights(self):
        """Carga los pesos guardados"""
        try:
            with open(self.weights_file, 'r') as f:
                weights = json.load(f)
                self.mlp.W1 = np.array(weights['W1'], dtype=np.float64)
                self.mlp.W2 = np.array(weights['W2'], dtype=np.float64)
                self.mlp.b1 = np.array(weights['b1'], dtype=np.float64)
                self.mlp.b2 = np.array(weights['b2'], dtype=np.float64)
                
                if weights['mean'] is not None:
                    self.mean = np.array(weights['mean'], dtype=np.float64)
                if weights['std'] is not None:
                    self.std = np.array(weights['std'], dtype=np.float64)
                    
                print("Pesos cargados exitosamente")
                return True
        except Exception as e:
            print(f"Error al cargar pesos: {e}")
            return False

    def save_weights(self, mean=None, std=None):
        """Guarda los pesos y parámetros de normalización"""
        weights = {
            'W1': self.mlp.W1.tolist(),
            'W2': self.mlp.W2.tolist(),
            'b1': self.mlp.b1.tolist(),
            'b2': self.mlp.b2.tolist(),
            'mean': mean.tolist() if mean is not None else self.mean.tolist() if self.mean is not None else None,
            'std': std.tolist() if std is not None else self.std.tolist() if self.std is not None else None
        }
        
        with open(self.weights_file, 'w') as f:
            json.dump(weights, f)
        print("Pesos guardados exitosamente")

    def predict(self, features):
        """Predice la clase para un conjunto de características"""
        # Convertir features a array de numpy
        X = np.array(features, dtype=np.float64)
        
        # Normalizar si es posible
        if self.mean is not None and self.std is not None:
            X = (X - self.mean) / (self.std + 1e-8)
        
        # Obtener predicción
        output = self.mlp.forward(X)
        prob = float(output[0][0])
        
        # Asegurar que la probabilidad esté entre 0 y 1
        prob = np.clip(prob, 0, 1)
        
        return {
            "clasificacion": "Spawn Bot" if prob > 0.5 else "Normal",
            "probabilidad": round(prob * 100, 2)
        }

# Instancia global del clasificador
classifier = MLPClassifier()

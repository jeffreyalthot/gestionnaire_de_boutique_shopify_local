from __future__ import annotations

try:
    import numpy as np
    from sklearn.linear_model import SGDRegressor
except ImportError:  # dépendances facultatives
    np = None
    SGDRegressor = None


class OnlineRegressor:
    def __init__(self, learning_rate: float = 0.01) -> None:
        self.fitted = False
        self.learning_rate = learning_rate
        self.weights: list[float] = []
        self.bias = 0.0
        self._accelerated = bool(np is not None and SGDRegressor is not None)
        self.model = SGDRegressor(random_state=42) if self._accelerated else None

    def partial_fit(self, x: list[list[float]], y: list[float]) -> None:
        if not x:
            return
        if len(x) != len(y):
            raise ValueError("x et y doivent avoir la même taille")
        if self._accelerated:
            self.model.partial_fit(np.asarray(x), np.asarray(y))
        else:
            width = len(x[0])
            if any(len(row) != width for row in x):
                raise ValueError("Dimensions de caractéristiques incohérentes")
            if not self.weights:
                self.weights = [0.0] * width
            for row, target in zip(x, y, strict=True):
                prediction = sum(weight * value for weight, value in zip(self.weights, row, strict=True)) + self.bias
                error = prediction - float(target)
                for index, value in enumerate(row):
                    self.weights[index] -= self.learning_rate * error * float(value)
                self.bias -= self.learning_rate * error
        self.fitted = True

    def predict(self, x: list[float], default: float = 0) -> float:
        if not self.fitted:
            return default
        if self._accelerated:
            return float(self.model.predict(np.asarray([x]))[0])
        if len(x) != len(self.weights):
            raise ValueError("Dimension de caractéristiques incohérente")
        return float(sum(weight * value for weight, value in zip(self.weights, x, strict=True)) + self.bias)

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

try:  # Accélération facultative; aucune dépendance lourde n'est requise.
    import numpy as np
    from sklearn.feature_extraction.text import HashingVectorizer
    from sklearn.linear_model import SGDClassifier
except ImportError:  # pragma: no cover - chemin testé par comportement
    np = None
    HashingVectorizer = None
    SGDClassifier = None


class OnlineTextClassifier:
    def __init__(self, classes: list[str], features: int = 2**15) -> None:
        if len(classes) < 2:
            raise ValueError("Au moins deux classes sont requises.")
        self.class_names = tuple(classes)
        self.fitted = False
        self._documents = Counter()
        self._tokens: dict[str, Counter[str]] = defaultdict(Counter)
        self._vocabulary: set[str] = set()
        self._accelerated = bool(np is not None and HashingVectorizer is not None and SGDClassifier is not None)
        if self._accelerated:
            self.classes = np.array(classes)
            self.vectorizer = HashingVectorizer(n_features=features, alternate_sign=False, norm="l2")
            self.model = SGDClassifier(loss="log_loss", random_state=42, average=True)
        else:
            self.classes = self.class_names
            self.vectorizer = None
            self.model = None

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]{2,}", text.lower())[:512]

    def partial_fit(self, texts: list[str], labels: list[str]) -> None:
        if not texts:
            return
        if len(texts) != len(labels):
            raise ValueError("texts et labels doivent avoir la même taille")
        unknown = set(labels) - set(self.class_names)
        if unknown:
            raise ValueError(f"Classes inconnues: {sorted(unknown)}")
        if self._accelerated:
            matrix = self.vectorizer.transform(texts)
            self.model.partial_fit(
                matrix,
                np.array(labels),
                classes=self.classes if not self.fitted else None,
            )
        else:
            for text, label in zip(texts, labels, strict=True):
                tokens = self._tokenize(text)
                self._documents[label] += 1
                self._tokens[label].update(tokens)
                self._vocabulary.update(tokens)
        self.fitted = True

    def predict(self, text: str) -> tuple[str, float]:
        if not self.fitted:
            return self.class_names[0], 0.0
        if self._accelerated:
            matrix = self.vectorizer.transform([text])
            label = str(self.model.predict(matrix)[0])
            probabilities = self.model.predict_proba(matrix)[0]
            return label, float(np.max(probabilities))
        tokens = self._tokenize(text)
        total_documents = sum(self._documents.values())
        vocabulary_size = max(1, len(self._vocabulary))
        scores: dict[str, float] = {}
        for label in self.class_names:
            prior = (self._documents[label] + 1) / (total_documents + len(self.class_names))
            token_total = sum(self._tokens[label].values())
            score = math.log(prior)
            for token in tokens:
                score += math.log((self._tokens[label][token] + 1) / (token_total + vocabulary_size))
            scores[label] = score
        best = max(scores, key=scores.get)
        maximum = scores[best]
        exp_values = {label: math.exp(value - maximum) for label, value in scores.items()}
        confidence = exp_values[best] / sum(exp_values.values())
        return best, float(confidence)

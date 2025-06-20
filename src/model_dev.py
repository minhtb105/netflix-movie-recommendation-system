import logging
from abc import ABC, abstractmethod

class Model(ABC):
    """
    Abstract class for all models
    """
    @abstractmethod
    def train(self, X_train, y_train):
        pass
    
class MatrixFactorization(Model):
    def train(self, X_train, y_train, **kwargs):
        pass
    
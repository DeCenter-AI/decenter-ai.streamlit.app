from io import BytesIO
from typing import Type, Union
from sklearn.linear_model import LinearRegression
from abc import ABC, abstractmethod


class ModelTrainer(ABC):
    dataset: Union[BytesIO, 'str']
    pretrained_model: BytesIO

    X, y = None, None
    X_train, X_test, y_tain, y_test = [None] * 4
    trained_model = None

    @abstractmethod
    def __post_init__(self):
        pass

    @abstractmethod
    def split_dataset(self, test_size=0.2, random_state=42, **kwargs):
        pass

    @abstractmethod
    def load_dataset(self):
        pass

    @abstractmethod
    def train_model(self) -> 'Model':
        pass

    @abstractmethod
    def calculate_score(self) -> float:
        pass

from typing import List
from abc import ABC, abstractmethod


class IDGetter(ABC):

    @abstractmethod
    def get_id(self):
        pass


class IDPool(List):

    def __init__(self, name, *args, **kwargs):
        super(IDPool, self).__init__(*args, **kwargs)
        self.is_filling = False
        self.name = name


class IDGetterError(Exception):
    pass

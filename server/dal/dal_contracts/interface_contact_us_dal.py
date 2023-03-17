from abc import ABC, abstractmethod


class IContactUsDal(ABC):
    @abstractmethod
    def __init__(self, app=None):
        pass

    @abstractmethod
    def add_contact_us(self, data):
        pass

    @abstractmethod
    def get_contact_us(self, filter_by=None, filter_value=None):
        pass
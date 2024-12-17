from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def getDatabase(self):
        pass

    @abstractmethod
    def closeDatabase(self):
        pass

    @abstractmethod
    def getCursor(self):
        pass
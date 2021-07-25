from abc import ABC, abstractmethod

class GeneralBackup(ABC):
    @abstractmethod
    def saveAll(guild_map):
        pass

    @abstractmethod
    def loadAll() -> dictionary:
        pass
    
        
    
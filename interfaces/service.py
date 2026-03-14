from abc import ABC, abstractmethod

class Service(ABC):
    @abstractmethod
    def getHealthy(self) -> bool:
        """
        Method to determine if service is alive and healthy.
        """
        # TODO: override this for task service impls with more in depth checks such as task queue checks etc.
        return True
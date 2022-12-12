from abc import ABC, abstractmethod


class ICircle2D(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_x(self) -> float:
        pass

    @abstractmethod
    def set_x(self, new_x) -> None:
        pass

    @abstractmethod
    def get_y(self) -> float:
        pass

    @abstractmethod
    def set_y(self, new_y) -> None:
        pass

    @abstractmethod
    def get_radius(self) -> float:
        pass

    @abstractmethod
    def set_radius(self, new_radius) -> None:
        pass
    
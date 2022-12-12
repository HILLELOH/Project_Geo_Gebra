from abc import ABC, abstractmethod


class IPoint2D(ABC):
    @abstractmethod
    def set_location(self, x: float, y: float) -> None:
        pass

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
    def move_point(self, new_x, new_y) -> None:
        pass

    @abstractmethod
    def distance_from(self, from_p) -> float:
        pass

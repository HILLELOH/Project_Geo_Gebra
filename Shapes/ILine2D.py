from abc import ABC, abstractmethod


class ILine2D(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_a_x(self) -> float:
        pass

    @abstractmethod
    def set_a_x(self, new_x) -> None:
        pass

    @abstractmethod
    def get_a_y(self) -> float:
        pass

    @abstractmethod
    def set_a_y(self, new_y) -> None:
        pass

    @abstractmethod
    def get_b_x(self) -> float:
        pass

    @abstractmethod
    def set_b_x(self, new_x) -> None:
        pass

    @abstractmethod
    def get_b_y(self) -> float:
        pass

    @abstractmethod
    def set_b_y(self, new_y) -> None:
        pass

    @abstractmethod
    def len(self, l) -> float:
        pass

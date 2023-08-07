import abc
from typing import Iterable, Tuple, Union, Protocol, Any, Callable, Union


class Tabular(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def as_map(self) -> Iterable[Tuple[str, Union[bool, int, float, str]]]:
        ...

    @abc.abstractmethod
    def as_tuple(self) -> tuple:
        ...

    class Constraints:
        ...


class SingletonProtocol(Protocol):
    """"""
    _singleton: Any

    def __call__(self, *args, **kwargs):
        pass


def provides_singleton(func: Any) -> SingletonProtocol:
    return func

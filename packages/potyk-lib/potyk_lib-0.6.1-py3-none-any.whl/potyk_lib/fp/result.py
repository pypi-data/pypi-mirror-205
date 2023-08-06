import dataclasses
from functools import partial
from typing import Generic, Any, cast, Iterable, Tuple, Optional, TypeVar, Iterator, Callable

__all__ = ['Result', 'Ok', 'Err']

T = TypeVar('T')

OkT = TypeVar('OkT')
ErrT = TypeVar('ErrT')
NewT = TypeVar('NewT')


class Result(Generic[OkT, ErrT]):
    def __iter__(self) -> Iterator[Tuple[Optional[OkT], Optional[ErrT]]]:
        if isinstance(self, Ok):
            return iter(cast(Iterable[Tuple[Optional[OkT], Optional[ErrT]]], (self.value, None)))
        elif isinstance(self, Err):
            return iter(cast(Iterable[Tuple[Optional[OkT], Optional[ErrT]]], (None, self.value)))
        else:
            raise RuntimeError('Наследовать Result могут только Ok и Err')

    def map(self, any_: Callable[[OkT], NewT]) -> 'Result[NewT, ErrT]':
        """
        >>> Ok(2).map(lambda v: v + 2)
        Ok(value=4)
        >>> Err(2).map(lambda v: v + 2)
        Err(value=2)
        """
        if isinstance(self, Err):
            return self
        else:
            return Result.safe(partial(any_, cast(Ok, self).value))

    def map_err(self, any_: Callable[[ErrT], NewT]) -> 'Result[OkT, NewT]':
        """
        >>> Ok(2).map_err(lambda v: v + 2)
        Ok(value=2)
        >>> Err(2).map_err(lambda v: v + 2)
        Err(value=4)
        """
        if isinstance(self, Ok):
            return self
        else:
            return Err(any_(cast(Err, self).value))

    def or_else(self, any_: Callable[[ErrT], 'Result[NewT, NewT]']) -> 'Result[OkT, NewT]':
        """
        >>> Ok(2).or_else(lambda v: Ok(v + 2))
        Ok(value=2)
        >>> Err(2).or_else(lambda v: Ok(v + 2))
        Ok(value=4)
        """
        if isinstance(self, Ok):
            return self
        else:
            return any_(cast(Err, self).value)

    def and_then(self, any_: Callable[[OkT], 'Result[NewT, NewT]']) -> 'Result[NewT, ErrT]':
        """
        >>> Ok(2).and_then(lambda v: Ok(v + 2))
        Ok(value=4)
        >>> Err(2).and_then(lambda v: Ok(v + 2))
        Err(value=2)
        """
        if isinstance(self, Ok):
            return any_(cast(Ok, self).value)
        else:
            return self

    @classmethod
    def safe(cls, callable_: Callable[[], OkT]) -> 'Result[OkT, Exception]':
        """
        >>> Result.safe(lambda: 2)
        Ok(value=2)
        >>> def raise_e():
        ...   raise Exception('err')
        >>> Result.safe(raise_e)
        Err(value=Exception('err'))
        """
        try:
            return Ok(callable_())
        except Exception as e:
            return Err(e)

    def flatten(self):
        if isinstance(self.value, Result):
            return self.value
        else:
            return self


@dataclasses.dataclass(frozen=True)
class Ok(Generic[T], Result[T, Any]):
    value: T = None


@dataclasses.dataclass(frozen=True)
class Err(Generic[T], Result[Any, T]):
    value: T = None

import dataclasses
from typing import TypeVar, Generic, Callable, Union, Optional

T = TypeVar('T')
V = TypeVar('V')

__all__ = ['Maybe', 'Some', 'Nothing', 'falsy', 'nullish']


class Maybe(Generic[T]):
    """
    >>> falsy(1).if_some(lambda i: i+1).val
    2
    >>> falsy(None).if_some(lambda i: i+1).val is None
    True
    >>> falsy(None).if_nothing(lambda: 1).val
    1
    """

    def map(self, callable_: Callable[[T], V]) -> 'Maybe[V]':
        """
        >>> Some(123).map(lambda a: a+1).val
        124
        >>> Nothing().map(lambda a: a+1).val is None
        True
        """
        if isinstance(self, Some):
            return Some(callable_(self.val))
        else:
            return self

    if_some = map

    def and_maybe(self, maybe_callable: Callable[[T], 'Maybe[V]']) -> 'Maybe[V]':
        """
        >>> falsy(True).and_maybe(lambda _: falsy(1)).val
        1
        >>> falsy(False).and_maybe(lambda _: falsy(1)).val is None
        True
        """
        if isinstance(self, Some):
            return maybe_callable(self.val)
        else:
            return Nothing()

    def if_nothing(self, callable_):
        """
        >>> Nothing().if_nothing(lambda : 1).val
        1
        >>> Some(2).if_nothing(lambda : 1).val
        2
        """
        if isinstance(self, Some):
            return self
        else:
            return Some(callable_())

    def __getattr__(self, item):
        """
        >>> falsy(None).attr is None
        True
        >>> list(falsy({'a': 1}).keys())
        ['a']
        """
        if isinstance(self, Some):
            return getattr(self.val, item)
        else:
            return None

    @classmethod
    def none_guess(cls, val: Optional[T]) -> 'Maybe[T]':
        """
        >>> isinstance(Maybe.none_guess(None), Nothing)
        True
        >>> isinstance(Maybe.none_guess(''), Some)
        True
        """

        return Nothing() if val is None else Some(val)

    @classmethod
    def falsy_guess(cls, val: T) -> 'Maybe[T]':
        """
        >>> isinstance(Maybe.falsy_guess(''), Nothing)
        True
        >>> isinstance(Maybe.falsy_guess(1), Some)
        True
        """
        return Nothing() if not val else Some(val)

    def or_else(self, maybe_callable: Callable[[], 'Maybe[V]']) -> 'Union[Maybe[T], Maybe[V]]':
        if isinstance(self, Some):
            return self
        else:
            return maybe_callable()

    def and_then(self, maybe_callable: Callable[[T], 'Maybe[V]']) -> 'Maybe[V]':
        """
        >>> falsy(1).and_then(lambda _: falsy(2)).get()
        2
        >>> falsy(1).and_then(lambda _: falsy(None)).get() is None
        True
        >>> falsy(None).and_then(lambda _: falsy(2)).get() is None
        True
        """
        if isinstance(self, Some):
            return maybe_callable(self.val)
        else:
            return self

    def or_(self, maybe: 'Maybe[V]') -> 'Union[Maybe[T], Maybe[V]]':
        if isinstance(self, Some):
            return self
        else:
            return maybe

    def unwrap(self) -> T:
        if isinstance(self, Some):
            return self.val
        else:
            raise ValueError('Нельзя вызвать unwrap для Nothing')

    def get(self) -> Optional[T]:
        """
        >>> falsy(None).get() is None
        True
        >>> falsy(1).get()
        1
        """
        return self.val if isinstance(self, Some) else None


nullish: Callable[[Optional[T]], Maybe[T]] = Maybe.none_guess
falsy: Callable[[T], Maybe[T]] = Maybe.falsy_guess


@dataclasses.dataclass(frozen=True)
class Some(Generic[T], Maybe[T]):
    val: T


class Nothing(Maybe):
    ...

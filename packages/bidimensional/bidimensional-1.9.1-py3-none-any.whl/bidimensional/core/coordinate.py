"""Coordinate class container module.

This module contains the Coordinate class, which is used to represent a 2D
coordinate. It is used by all classes in the `bidimensional` package and
presents many similarities to the builtin `tuple` class.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

from math import ceil, floor, trunc
from typing import Any, Dict, Generator, Sequence, Union

import matplotlib.pyplot as plt


class Coordinate(Sequence):
    """Real-value, bidimensional coordinate.

    This class represents a two-dimensional coordinate. Its main purpose is to
    serve as a normalized conversion format for data going in and out of the
    scripts contained in the project.

    Args:
        x (float): the x value of the coordinate.
        y (float): the y value of the coordinate.
        STYLES (Dict[str, Any]): the dictionary containing default matplotlib
            styles for coordinate plotting.
    """

    __slots__ = ("_x", "_y")

    STYLES: Dict[str, Any] = {
        "color": "#396fe3",
        "ms": 10
    }

    def __init__(self, x: Union[int, float], y: Union[int, float]) -> None:
        """Initialize a coordinate instance.

        Args:
            x (Union[int, float]): the X component of the coordinate.
            y (Union[int, float]): the Y component of the coordinate.
        """
        self.x: float = x
        self.y: float = y

    @property
    def x(self) -> float:
        """Get the X component of the coordinate.

        Returns:
            float: the X component of the coordinate.
        """
        return self._x

    @x.setter
    def x(self, value: Union[int, float]) -> None:
        """Set the X component of the coordinate.

        Args:
            value (Union[int, float]): the X component of the coordinate.

        Raises:
            TypeError: if `value` is not a type `int` or `float`.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected \"int\" or \"float\", "
                + f"got \"{value.__class__.__name__}\""
            )

        self._x = float(value)

    @property
    def y(self) -> float:
        """Get the Y component of the coordinate.

        Returns:
            float: the Y component of the coordinate.
        """
        return self._y

    @y.setter
    def y(self, value: Union[int, float]) -> None:
        """Set the X component of the coordinate.

        Args:
            value (Union[int, float]): the X component of the coordinate.

        Raises:
            TypeError: if `value` is not a type `int` or `float`.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected \"int\" or \"float\", "
                + f"got \"{value.__class__.__name__}\""
            )

        self._y = float(value)

    def plot(self, *args, ax=None, annotate=False, **kwargs) -> None:
        """Plot the coordinate.

        Args:
            *args (tuple): Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None (if None, the current axes will be used).
            annotate (bool, optional): Whether to annotate the coordinate.
            **kwargs (dict): Keyword arguments to pass to the plot
        """
        styles = self.STYLES.copy()
        styles.update(kwargs)
        shape = args[0] if args else '.'
        ax = plt.gca() if ax is None else ax

        if annotate:
            ax.annotate(f"({self._x:.4f}, {self._y:.4f})", (self._x, self._y))

        ax.plot(self._x, self._y, shape, **styles)

    def __add__(self, value: Coordinate) -> Coordinate:
        """Add two coordinates.

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self._x + value.x, self._y + value.y)

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __sub__(self, value: Coordinate) -> Coordinate:
        """Subtract two coordinates.

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self._x - value.x, self._y - value.y)

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __mul__(self, value: Coordinate) -> Coordinate:
        """Multiply two coordinates.

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * value.y)

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __truediv__(self, value: Coordinate) -> Coordinate:
        """Divide two coordinates (floating point).

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * -value.y)

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __floordiv__(self, value: Coordinate) -> Coordinate:
        """Divide two coordinates (floor result).

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            temp = floor(self / value)
            return Coordinate(temp.x, temp.y)
        self.__class__.__name__

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __mod__(self, value: Coordinate) -> Coordinate:
        """Modulus of two coordinates.

        Args:
            value (Coordinate): the other coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        if isinstance(value, Coordinate):
            temp = (self / value - self // value) * value
            return Coordinate(temp.x, temp.y)

        raise TypeError(
            f"expected \"{self.__class__.__name__}\", "
            + f"got \"{value.__class__.__name__}\""
        )

    def __neg__(self) -> Coordinate:
        """Negate a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(-self._x, -self._y)

    def __pos__(self) -> Coordinate:
        """Positivize a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(+self._x, +self._y)

    def __abs__(self) -> Coordinate:
        """Return the absolute value of a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(abs(self._x), abs(self._y))

    def __round__(self, n: int = 0) -> Coordinate:
        """Round a coordinate.

        Args:
            n (int, optional): the digits of precission for the rounding
                operation. Defaults to 0.

        Returns:
            Coordinate: the result of the operation.
        """
        if not isinstance(n, int):
            raise TypeError("n must be an int.")

        return Coordinate(round(self._x, n), round(self._y, n))

    def __floor__(self) -> Coordinate:
        """Floor a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(floor(self._x), floor(self._y))

    def __ceil__(self) -> Coordinate:
        """Ceil a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(ceil(self._x), ceil(self._y))

    def __trunc__(self) -> Coordinate:
        """Truncate a coordinate.

        Returns:
            Coordinate: the result of the operation.
        """
        return Coordinate(trunc(self._x), trunc(self._y))

    def __eq__(self, value: object) -> bool:
        """Compare the equality of two objects.

        Args:
            value (object): the other coordinate.

        Returns:
            bool: the result of the operation.
        """
        if not isinstance(value, Coordinate):
            raise TypeError(
                f"expected \"{self.__class__.__name__}\", "
                + f"got \"{value.__class__.__name__}\""
            )

        return self._x == value.x and self._y == value.y

    def __ne__(self, value: object) -> bool:
        """Compare the inequality of two objects.

        Args:
            value (object): the other coordinate.

        Returns:
            bool: the result of the operation.
        """
        if not isinstance(value, Coordinate):
            raise TypeError(
                f"expected \"{self.__class__.__name__}\", "
                + f"got \"{value.__class__.__name__}\""
            )

        return self._x != value.x or self._y != value.y

    def __str__(self) -> str:
        """Convert the coordinate to a string.

        Returns:
            str: the coordinate as a string.
        """
        return f"Coordinate({self._x}, {self._y})"

    def __repr__(self) -> str:
        """Obtain the string representation of the coordinate.

        Returns:
            str: the string representation of the coordinate.
        """
        return f"Coordinate({self._x}, {self._y})"

    def __hash__(self) -> int:
        """Obtain the hash of the coordinate.

        Returns:
            int: the hash of the coordinate.
        """
        return hash((self._x, self._y))

    def __bool__(self) -> bool:
        """Obtain the boolean value of the coordinate.

        Returns:
            bool: the boolean value of the coordinate.
        """
        return self._x != 0 or self._y != 0

    def __len__(self) -> int:
        """Obtain the amount of terms in the coordinate.

        Returns:
            int: the amount of terms in the coordinate.
        """
        return 2

    def __getitem__(self, index: Union[int, slice]) -> Any:
        """Get the X, Y coordinate components via index or slice.

        Args:
            index (Union[int, slice]): the index or slice of the component(s).

        Returns:
            Any: the value(s) of the component(s).

        Raises:
            IndexError: if the index of the component is not 0 or 1.
            TypeError: if the index is not an int or a slice.
        """
        if isinstance(index, int):
            if index == 0:
                return self._x
            elif index == 1:
                return self._y
            else:
                raise IndexError("index must be 0 (x) or 1 (y)")

        elif isinstance(index, slice):
            return (self._x, self._y)[index]

        else:
            raise TypeError("index must be an int or a slice.")

    def __setitem__(self, index: Union[int, slice], value: Union[int, float]) -> None:
        """Set the X or Y coordinate components via index or slice.

        Args:
            index (Union[int, slice]): the index or slice of the component(s).
            value (Union[int, float]): the new value(s) of the component(s).

        Raises:
            IndexError: if the index of the component is not 0 or 1.
            NotImplementedError: if the index is a slice.
        """
        if isinstance(index, int):
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            else:
                raise IndexError("index must be 0 (x) or 1 (y)")

        elif isinstance(index, slice):
            raise NotImplementedError(
                "slice attribute assignment is not supported"
            )

        else:
            raise TypeError("index must be an int or a slice.")

    def __iter__(self) -> Generator[float, None, None]:
        """Obtain the iterable of the coordinate.

        Returns:
            Generator[float, None, None]: the iterable of the coordinate.
        """
        yield self._x
        yield self._y

    def __reversed__(self) -> Generator[float, None, None]:
        """Obtain the reversed iterable of the coordinate.

        Returns:
            Generator[float, None, None]: the reversed iterable of the
                coordinate.
        """
        yield self._y
        yield self._x

    def __copy__(self) -> Coordinate:
        """Copy the coordinate.

        Returns:
            Coordinate: the copy of the coordinate.
        """
        return self.__class__(self._x, self._y)

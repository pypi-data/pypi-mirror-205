from typing import Callable, Optional, TypeVar

import equinox as eqx


T = TypeVar("T")


class Functional(eqx.Module):
    """General Function"""

    _name: str
    _fn: Callable[..., T]
    _pipe_type: str

    def __init__(
        self,
        fn: Optional[Callable[..., T]] = None,
        pipe_type: str = "normal",
        name: str = "Func",
    ):
        """Make a General Function.

        Args:
            name (str, optional): Name of the function. Defaults to "Func".
            pipe_type: Type of the function.(vmap or pmap or jit or normal) Defaults to "normal".
            fn (Optional[Callable|None], optional): Callable object.
        """
        super().__init__()
        self._name = name
        self._fn = fn
        self._pipe_type = pipe_type

    @property
    def name(self):
        """Get the name of the function."""
        return self._name

    @property
    def func(self):
        """Get the function."""
        return self._fn

    @property
    def piep_type(self):
        """Get the type of the function."""
        return self._pipe_type

    def desc(self):
        """Description for the function."""
        return self.__repr__()

    def __call__(self, *args, **kwargs):
        """Call the function with given arguments."""
        if self._fn is None:
            raise ValueError("No Callable Function to Call")
        return self._fn(*args, **kwargs)

    def __rshift__(self, _next: Callable):
        """Make Pipe.

        Create a pipe between this function and the next one.

        Args:
            _next (Functional): The next function in the pipe.

        Returns:
            Pipe: A pipe between this function and the next one.
        """
        from .pipe import Pipe

        if not isinstance(_next, Functional):
            if hasattr(_next, "__name__"):
                _next = Functional(name=_next.__name__, fn=_next)
            else:
                _next = Functional(name="Function", fn=_next)

        return Pipe([self, _next])


class StateFunc(Functional):
    """Class for state function.

    Args:
        name (str): Name of the state function.
        fn (Optional[Callable]): Function to be called.
    """

    def __init__(
        self,
        fn: Optional[Callable[..., T]] = None,
        name: str = "State",
    ):
        """Initialize the state function."""
        super().__init__(fn=fn, name=name)

    def __repr__(self):
        """Return a string representation of the state function."""
        return super().__repr__()

    def _tree_flatten(self):
        """Flatten the tree structure of the state function."""
        return super()._tree_flatten()

    def _summary(self):
        """Print a summary of the state function."""
        pass

    def _predict(self, *args, **kwargs):
        """Predict"""
        pass

    def __call__(self, *args, **kwargs):
        """Call the state function."""
        return self.func(*args, **kwargs)

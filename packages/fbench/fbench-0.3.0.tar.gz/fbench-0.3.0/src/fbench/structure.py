from typing import Callable, NamedTuple, Optional, Tuple

import numpy as np

__all__ = ("CoordinateMatrices",)


class CoordinateMatrices(NamedTuple):
    """An immutable data structure for X, Y, Z coordinate matrices."""

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray


class FunctionConfig(NamedTuple):
    """An immutable data structure for a function configuration."""

    func: Callable[[np.ndarray], float]
    x_bounds: Tuple[float, float]
    y_bounds: Tuple[float, float]
    global_minimum_x: Optional[np.ndarray]
    global_minimum_fx: Optional[float]

import numpy as np
import toolz

from fbench import function, structure

__all__ = ("FUNCTION_CONFIGURATIONS",)


FUNCTION_CONFIGURATIONS = {
    "Ackley": structure.FunctionConfig(
        func=function.ackley,
        x_bounds=(-5, 5),
        y_bounds=(-5, 5),
        global_minimum_x=(0, 0),
        global_minimum_fx=0,
    ),
    "Rastrigin": structure.FunctionConfig(
        func=function.rastrigin,
        x_bounds=(-5.12, 5.12),
        y_bounds=(-5.12, 5.12),
        global_minimum_x=(0, 0),
        global_minimum_fx=0,
    ),
    "Rosenbrock": structure.FunctionConfig(
        func=function.rosenbrock,
        x_bounds=(-2, 2),
        y_bounds=(-2, 2),
        global_minimum_x=(1, 1),
        global_minimum_fx=0,
    ),
    "Rosenbrock_log1p": structure.FunctionConfig(
        func=toolz.compose_left(function.rosenbrock, np.log1p),
        x_bounds=(-2, 2),
        y_bounds=(-2, 2),
        global_minimum_x=(1, 1),
        global_minimum_fx=0,
    ),
    "Sphere": structure.FunctionConfig(
        func=function.sphere,
        x_bounds=(-2, 2),
        y_bounds=(-2, 2),
        global_minimum_x=(0, 0),
        global_minimum_fx=0,
    ),
}

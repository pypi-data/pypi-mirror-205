import numpy as np

from fbench import exception

__all__ = ("check_vector",)


def check_vector(x, /, *, min_elements):
    """Validate an n-dimensional vector.

    Parameters
    ----------
    x : array_like
        Input data with :math:`n` elements that can be converted to an array.
    min_elements : int
        Specify the minimum number of elements ``x`` must have.

    Returns
    -------
    np.ndarray
        The :math:`n`-dimensional vector.

    Raises
    ------
    NotAVectorError
        If ``x`` is not vector-like.
    IncorrectNumberOfElements
        If ``x`` does not satisfy the ``min_elements`` condition.
    """
    x = np.asarray(x)

    if len(x.shape) != 1:
        raise exception.NotAVectorError(
            f"input must be vector-like object - it has shape={x.shape}"
        )

    if not len(x) >= min_elements:
        raise exception.IncorrectNumberOfElements(
            f"number of elements must be at least {min_elements} "
            f"- it has {x.shape[0]}"
        )

    return x

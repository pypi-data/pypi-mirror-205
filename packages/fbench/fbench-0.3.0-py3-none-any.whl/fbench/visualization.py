from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import toolz
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from fbench import structure, validation

__all__ = (
    "PlotConfig",
    "create_contour_plot",
    "create_coordinates3d",
    "create_surface_plot",
)


class PlotConfig(Enum):
    """Configurations for plotting."""

    @classmethod
    def get_kws_contour__base(cls):
        """Returns kwargs for ``contour``: base configuration."""
        return dict(
            levels=12,
            colors="dimgray",
            antialiased=True,
            linewidths=0.25,
            alpha=1.0,
            zorder=1,
        )

    @classmethod
    def get_kws_contourf__base(cls):
        """Returns kwargs for ``contourf``: base configuration."""
        return dict(
            levels=100,
            antialiased=True,
            alpha=0.61803,
            zorder=0,
        )

    @classmethod
    def get_kws_contourf__YlOrBr(cls):
        """Returns kwargs for ``contourf``: YlOrBr configuration for dark max."""
        output = dict(
            cmap=cm.YlOrBr,
        )
        output.update(cls.get_kws_contourf__base())
        return output

    @classmethod
    def get_kws_contourf__YlOrBr_r(cls):
        """Returns kwargs for ``contourf``: YlOrBr_r configuration for dark min."""
        output = dict(
            cmap=cm.YlOrBr_r,
        )
        output.update(cls.get_kws_contourf__base())
        return output

    @classmethod
    def get_kws_surface__base(cls):
        """Returns kwargs for ``plot_surface``: base configuration."""
        return dict(
            rstride=1,
            cstride=1,
            edgecolors="dimgray",
            antialiased=True,
            linewidth=0.1,
            alpha=0.61803,
            zorder=0,
        )

    @classmethod
    def get_kws_surface__YlOrBr(cls):
        """Returns kwargs for ``plot_surface``: YlOrBr configuration for dark max."""
        output = dict(
            cmap=cm.YlOrBr,
        )
        output.update(cls.get_kws_surface__base())
        return output

    @classmethod
    def get_kws_surface__YlOrBr_r(cls):
        """Returns kwargs for ``plot_surface``: YlOrBr_r configuration for dark min."""
        output = dict(
            cmap=cm.YlOrBr_r,
        )
        output.update(cls.get_kws_surface__base())
        return output


@toolz.curry
def create_contour_plot(coord, /, *, kws_contourf=None, kws_contour=None, ax=None):
    """Create a contour plot from X, Y, Z coordinate matrices.

    Parameters
    ----------
    coord : CoordinateMatrices
        The X, Y, Z coordinate matrices to plot.
    kws_contourf : dict of keyword arguments, default=None
        The kwargs are passed to ``matplotlib.axes.Axes.contourf``.
        By default, using configuration: ``PlotConfig.get_kws_contourf__YlOrBr_r()``.
        Optionally specify a dict of keyword arguments to update configurations.
    kws_contour : dict of keyword arguments, default=None
        The kwargs are passed to ``matplotlib.axes.Axes.contour``.
        By default, using configuration: ``PlotConfig.get_kws_contour__base()``.
        Optionally specify a dict of keyword arguments to update configurations.
    ax: matplotlib.axes.Axes, default=None
        Optionally supply an ``Axes`` object.
        If None, the current ``Axes`` object is retrieved.

    Returns
    -------
    matplotlib.axes.Axes
        The ``Axes`` object with filled contours and superimposed contour lines.

    Notes
    -----
    - Function is curried.
    - Examples are shown in the
      `Overview of fBench functions <https://fbench.readthedocs.io/en/stable/fBench-functions.html)>`_.
    """  # noqa: E501
    ax = ax or plt.gca()

    settings_contourf = PlotConfig.get_kws_contourf__YlOrBr_r()
    settings_contourf.update(kws_contourf or dict())
    contour_plot = ax.contourf(coord.x, coord.y, coord.z, **settings_contourf)

    settings_contour = PlotConfig.get_kws_contour__base()
    settings_contour.update(kws_contour or dict())
    ax.contour(coord.x, coord.y, coord.z, **settings_contour)

    plt.colorbar(
        contour_plot,
        cax=make_axes_locatable(ax).append_axes("right", size="5%", pad=0.15),
    )

    return ax


@toolz.curry
def create_coordinates3d(func, x_coord, y_coord=None, /):
    """Create X, Y, Z coordinate matrices from coordinate vectors and function.

    First, a meshgrid of (x, y)-coordinates is constructed from the coordinate vectors.
    Then, the z-coordinate for each (x, y)-point is computed using the function.

    Parameters
    ----------
    func : Callable[[np.ndarray], float]
        A scalar-valued function that takes a two-dimensional, real vector as input.
    x_coord : np.ndarray
        An one-dimensional array for the x-coordinates of the grid.
    y_coord : np.ndarray, default=None
        An one-dimensional array for the y-coordinates of the grid.
        If None, ``y_coord`` equals ``x_coord``.

    Returns
    -------
    CoordinateMatrices
        The coordinate matrices.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> import fbench
    >>> fbench.create_coordinates3d(fbench.sphere, [-1, 0, 1])
    CoordinateMatrices(x=array([[-1,  0,  1],
           [-1,  0,  1],
           [-1,  0,  1]]), y=array([[-1, -1, -1],
           [ 0,  0,  0],
           [ 1,  1,  1]]), z=array([[2., 1., 2.],
           [1., 0., 1.],
           [2., 1., 2.]]))
    """
    x_coord = validation.check_vector(x_coord, min_elements=2)
    y_coord = (
        x_coord if y_coord is None else validation.check_vector(y_coord, min_elements=2)
    )
    x, y = np.meshgrid(x_coord, y_coord)
    z = np.apply_along_axis(func1d=func, axis=1, arr=np.c_[x.ravel(), y.ravel()])
    return structure.CoordinateMatrices(x, y, z.reshape(x.shape))


@toolz.curry
def create_surface_plot(coord, /, *, kws_surface=None, kws_contourf=None, ax=None):
    """Create a surface plot from X, Y, Z coordinate matrices.

    Parameters
    ----------
    coord : CoordinateMatrices
        The X, Y, Z coordinate matrices to plot.
    kws_surface : dict of keyword arguments, default=None
        The kwargs are passed to ``mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface``.
        By default, using configuration: ``PlotConfig.get_kws_surface__YlOrBr_r()``.
        Optionally specify a dict of keyword arguments to update configurations.
    kws_contourf : dict of keyword arguments, default=None
        The kwargs are passed to ``mpl_toolkits.mplot3d.axes3d.Axes3D.contourf``.
        By default, using configuration: ``PlotConfig.get_kws_contourf__YlOrBr_r()``.
        Optionally specify a dict of keyword arguments to update configurations.
    ax: mpl_toolkits.mplot3d.axes3d.Axes3D, default=None
        Optionally supply an ``Axes3D`` object.
        If None, the current ``Axes3D`` object is retrieved.

    Returns
    -------
    ax : mpl_toolkits.mplot3d.axes3d.Axes3D
        The ``Axes3D`` object of the surface.

    Notes
    -----
    - Function is curried.
    - Examples are shown in the
      `Overview of fBench functions <https://fbench.readthedocs.io/en/stable/fBench-functions.html)>`_.
    """  # noqa: E501
    ax = ax or plt.gcf().add_subplot(projection="3d")

    # Make background and axis panes transparent
    ax.patch.set_alpha(0.0)
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

    settings_surface = PlotConfig.get_kws_surface__YlOrBr_r()
    settings_surface.update(kws_surface or dict())
    ax.plot_surface(coord.x, coord.y, coord.z, **settings_surface)

    settings_contourf = PlotConfig.get_kws_contourf__YlOrBr_r()
    settings_contourf.update(kws_contourf or dict())
    settings_contourf["zdir"] = settings_contourf.get("zdir", "z")
    settings_contourf["offset"] = settings_contourf.get("offset", 0) + coord.z.min()
    ax.contourf(coord.x, coord.y, coord.z, **settings_contourf)

    return ax

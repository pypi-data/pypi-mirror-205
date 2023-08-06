#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import numpy as np


def scaled_coordinate(value, axis, scales, grids):
    # we want 0 to be top left edge, not center of top left pixel/vector:
    corrected = value + 0.5
    grid = 1 if grids is None else getattr(grids, axis)
    scale = getattr(scales, axis)
    return corrected * grid * scale.slope + scale.offset


def prettify_plot(fig, scales, grids=None):
    """
    Adorns a given figure with labels and a color bar.
    Also sets exactly two ticks on each axis (one at each end)
    to make the data range clearly visible, and rounds their labels
    if possible without them becoming indistinguishable.
    """
    from matplotlib.ticker import FuncFormatter, LinearLocator

    [ax] = fig.axes
    ax.xaxis.set_major_locator(LinearLocator(2))
    ax.yaxis.set_major_locator(LinearLocator(2))

    def make_formatter(axis, *, rounded):
        @FuncFormatter
        def formatter(value, _=None):
            scaled = scaled_coordinate(value, axis, scales, grids)
            return f"{scaled:.2f}" if rounded else f"{scaled}"
        return formatter

    def determine_suitable_formatter(axis):
        if axis == "x":
            ticks = ax.get_xticks()
        else:
            ticks = ax.get_yticks()
        first, last = ticks  # we expect there to be exactly two ticks
        # if ticks have same label after rounding, then don't round
        formatter = make_formatter(axis, rounded=True)
        if formatter(first) == formatter(last):
            formatter = make_formatter(axis, rounded=False)
        return formatter

    ax.xaxis.set_major_formatter(determine_suitable_formatter("x"))
    ax.yaxis.set_major_formatter(determine_suitable_formatter("y"))

    ax.set_xlabel(scales.x.label())
    ax.set_ylabel(scales.y.label())

    [image] = ax.images
    colorbar = fig.colorbar(image)
    colorbar.ax.yaxis.labelpad = 15
    colorbar.ax.set_ylabel(scales.i.label(), rotation=270)


def plot_image(data, scales, *, show=True):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.imshow(data)

    prettify_plot(fig, scales)

    if show:
        plt.show()
    else:
        return fig


def plot_vector_field(uvw_unscaled, uvw_scaled, is_3c, scales, grids, *, show=True):
    import matplotlib.pyplot as plt

    u = uvw_scaled["u"]
    v = uvw_scaled["v"]
    if is_3c:
        w = uvw_scaled["w"]

    if is_3c:
        background = np.ma.sqrt(u * u + v * v + w * w)
    else:
        background = np.ma.sqrt(u * u + v * v)

    fig, ax = plt.subplots()
    ax.imshow(background)
    ax.quiver(uvw_unscaled["u"], uvw_unscaled["v"], angles='xy', width=0.002)

    prettify_plot(fig, scales, grids)

    if show:
        plt.show()
    else:
        return fig

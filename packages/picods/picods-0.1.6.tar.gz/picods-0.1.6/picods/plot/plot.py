from typing import Iterable
from typing import List
from typing import Union

import matplotlib.pyplot as plt


def picoplot(
    title: str,
    xs: Iterable[Iterable],
    ys: Iterable[Iterable],
    legends: List[str],
    colors: List[str],
    x_label: str,
    y_label: str,
    x_lim: Union[int, None] = None,
    y_lim: Union[int, None] = None,
) -> None:
    """
    Plot a graph.

    Args:
        xs: The x values.
        ys: The y values.
        legends: The legends.
        colors: The colors.
        x_label: The x label.
        y_label: The y label.
        title: The title.
        x_lim: The x limit.
        y_lim: The y limit.
    """

    plt.figure(figsize=(16, 0.5 * len(xs[0]) + 0.5))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_lim:
        plt.xlim(0, x_lim)
    if y_lim:
        plt.ylim(0, y_lim)

    for x, y, color in zip(xs, ys, colors):
        plt.plot(x, y, color=color)

    plt.legend(legends)
    plt.show()

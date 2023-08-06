# picods (pico data science) Python Library

picods is a small data science visualization tool Python library that provides
two functions - picoplot and picotable - to generate plots and tables using
matplotlib and pandas. This library is ideal for quick and simple data
exploration and visualization tasks.

## Installation

The recommended way to install picods is via pip, which will download and
install the latest stable release from PyPI:

```bash
pip install picods
```

Alternatively, you can clone the repository from GitHub and install it manually:

```bash
git clone https://github.com/Tomcat-42/picods.git
cd picods
python setup.py install
```

## Usage

To use picods in your Python scripts, simply import the picods module and call
either the picoplot or picotable function:

```python
import picods

# Generate a plot
picods.picoplot(title, xs, ys, legends, colors, x_label, y_label, x_lim, y_lim)

# Generate a table
picods.picotable(title, rows, columns_labels, row_labels, round_digits, color)
```

### picoplot

The picoplot function generates a plot using the specified data, labels, colors,
and limits for the x and y axis. The function signature is as follows:

```python
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
) -> None
```

- title: The title of the plot
- xs: An iterable of iterables containing the x values for each series
- ys: An iterable of iterables containing the y values for each series
- legends: A list of strings containing the legend labels for each series
- colors: A list of strings containing the color codes for each series
- x_label: The label for the x-axis
- y_label: The label for the y-axis
- x_lim: An optional integer value to set the limit of the x-axis
- y_lim: An optional integer value to set the limit of the y-axis The available

plot types are:

- Line plot

### picotable

The picotable function generates a table using the specified data, row and
column labels, and round digits. The function signature is as follows:

```python
def picotable(
    title: str,
    rows: List[List[Union[Number, str]]],
    columns_labels: List[str],
    row_labels: List[str],
    round_digits: int = 4,
    color: str = "white",
) -> None
```

- title: The title of the table
- rows: A list of lists containing the data for the table
- columns_labels: A list of strings containing the labels for each column
- row_labels: A list of strings containing the labels for each row
- round_digits: An optional integer value to set the number of decimal places to
  round the data to
- color: An optional string value to set the background color of the table

## Examples

Here are some examples of how to use the picoplot and picotable functions:

```python
from picods import (picoplot, picotable)

picotable("table", [[0,1], [0,1]],["col1","col2"], ["row1", "row2"], round_digits=4, "white" )
picoplot("plot", [[0,1,2], [0,1,2]] ,[[1, 2, 4], [0, 2, 4]],["y = 2^x", "y=2*x"], ["red", "blue"], "x label", "y label")
```

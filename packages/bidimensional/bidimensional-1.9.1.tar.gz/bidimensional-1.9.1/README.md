# Bidimensional

[![PyPI release](https://github.com/erlete/bidimensional/actions/workflows/python-publish.yml/badge.svg)](https://github.com/erlete/bidimensional/actions/workflows/python-publish.yml) [![Python Test Execution](https://github.com/erlete/bidimensional/actions/workflows/python-tests.yml/badge.svg)](https://github.com/erlete/bidimensional/actions/workflows/python-tests.yml)

This package contains a collection of useful classes and functions for working with 2D geometry in Python.

## Objectives and contributions

This package has three fundamental bases:

* **Simplicity** - The package is designed to be simple and easy to use, with a minimalistic approach to the implementation of its features.
* **Rich documentation** - The package is fully documented, with a detailed description of its features and their usage.
* **Performance** - The package is designed to be as fast as possible, mainly using simple algebraic operations instead of complex calculations.

Any contribution is welcome as long as it follows the objectives of the package. For more information, refer to the [contributing guidelines](CONTRIBUTING.md).

## Features

The following features are currently implemented:

* `Coordinate` - A class for representing a 2D coordinate. It can be used to represent a point in the plane, or a vector from the origin. It provides with multiple access methods, as well as a set of useful methods for performing operations with other coordinates.
* `polygons.Triangle` - A class for representing a triangle in the plane. Contains several methods that can be used to compute its area, perimeter and relevant centers, as well as determining relevant properties of triangles (e.g. if they are equilateral, isosceles, etc.).
* `functions.Spline` - A class for representing a spline function. It can be used to interpolate a set of points in the plane and to compute the value of the function at any given point in between.
* `operations` - A module that contains relevant functions for performing operations with coordinates and triangles. It provides with functions for computing the distance between two points, the area of a triangle, the midpoint of a segment, etc.

## Installation

The installation process is performed via PyPI (Python Package Index), so the package can be installed using the `pip` command.

```bash
pip install bidimensional
```

_Refer to the [PyPI release](https://pypi.org/project/bidimensional) for more information about how to install the package in your system._

## Usage

Once the package has been installed, its modules can be easily imported into custom programs via the `import` statement.

## Examples

Composition of a small triangle out of the midpoints of the sides of a larger triangle, computation of the circumcircle of the inner triangle and figure plotting.

```python
import bidimensional.operations as op
import matplotlib.pyplot as plt

from bidimensional import Coordinate
from bidimensional.polygons import Triangle


outer_triangle = Triangle(
    Coordinate(0, 0),
    Coordinate(1, 0),
    Coordinate(0, 1)
)

inner_triangle = Triangle(
    op.midpoint(outer_triangle.a, outer_triangle.b),
    op.midpoint(outer_triangle.b, outer_triangle.c),
    op.midpoint(outer_triangle.c, outer_triangle.a)
)

outer_triangle.plot(color="darkorange", lw=2)
inner_triangle.plot()

plt.gca().add_patch(plt.Circle(
    inner_triangle.circumcenter,
    inner_triangle.circumradius,
    color="darkblue",
    fill=False,
    lw=2
))

plt.axis("equal")
plt.grid()
plt.show()
```

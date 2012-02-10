
=================
Lights Out solver
=================

A Python solver of the `Lights Out game <http://en.wikipedia.org/wiki/Lights_Out_(game)>`_
for a square board of arbitrary size *n*.

The solver works by inverting the adjacency matrix
of a grid graph of the size of the board. The matrix is defined over the
Galois Field GF(2), and the inversion is performed in this field using
Gauss-Jordan elimination.

For some board sizes *n* (eg., &n&=5) the adjacency matrix is rank deficient.
This means that for those sizes, some initial configurations have no
solution, and some other configurations have several solutions. The solver
determines if a given configuration is solvable. In that case,
it finds the simpler solution, ie., the solution with the minimum number
of movements. To do this, it also computes a base of the right null space of
the adjacency matrix.

Usage
=====

The module `lightsout.py` implements the solver. The class `lightsout.LighsOut`
offers a simple interface to the module. See the function `lightsout.main`
for an example.

You can also try the Lights Out solver with a simple GUI using
the script `lightsoutgui.py`. Execute the script with::

    $ python lightsoutgui.py 5

The first parameter indicates the board size. If omitted, it defaults to 5.

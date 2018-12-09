# coding: utf-8

"""
Automatic solver for Lights Out puzzles.
Currently only square grids are supported.

Includes a Gauss-Jordan elimination method for matrices
defined on arbitrary fields. In particular, the function
GF2inv inverts a matrix defined over the Galois Field GF(2) and
determines its null-space.
"""

from operator import add
from itertools import chain, combinations
from functools import reduce

import numpy as np
from scipy import ndimage


class GF2(object):
    """Galois field GF(2)."""
    
    def __init__(self, a=0):
        self.value = int(a) & 1
    
    def __add__(self, rhs):
        return GF2(self.value + GF2(rhs).value)
    
    def __mul__(self, rhs):
        return GF2(self.value * GF2(rhs).value)
    
    def __sub__(self, rhs):
        return GF2(self.value - GF2(rhs).value)
    
    def __truediv__(self, rhs):
        return GF2(self.value / GF2(rhs).value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value == rhs.value
        return self.value == rhs
    
    def __le__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value <= rhs.value
        return self.value <= rhs
    
    def __lt__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value < rhs.value
        return self.value < rhs
    
    def __int__(self):
        return self.value
    
    def __long__(self):
        return self.value
    

GF2array = np.vectorize(GF2)


def gjel(A):
    """Gauss-Jordan elimination."""
    nulldim = 0
    for i, row1 in enumerate(A):
        pivot = A[i:, i].argmax() + i
        if A[pivot, i] == 0:
            nulldim = len(A) - i
            break
        new_row = A[pivot] / A[pivot, i]
        A[pivot] = A[i]
        row1[:] = new_row
        
        for j, row2 in enumerate(A):
            if j == i:
                continue
            row2[:] -= new_row*A[j, i]
    return A, nulldim


def GF2inv(A):
    """Inversion and eigenvectors of the null-space of a GF2 matrix."""
    n = len(A)
    assert n == A.shape[1], "Matrix must be square"
    
    A = np.hstack([A, np.eye(n)])
    B, nulldim = gjel(GF2array(A))
    
    inverse = np.int_(B[-n:, -n:])
    E = B[:n, :n]
    null_vectors = []
    if nulldim > 0:
        null_vectors = E[:, -nulldim:]
        null_vectors[-nulldim:, :] = GF2array(np.eye(nulldim))
        null_vectors = np.int_(null_vectors.T)
    
    return inverse, null_vectors


def lightsoutbase(n):
    """Base of the LightsOut problem of size (n,n)"""
    a = np.eye(n*n)
    a = np.reshape(a, (n*n, n, n))
    a = np.array(list(map(ndimage.binary_dilation, a)))
    return np.reshape(a, (n*n, n*n))


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class LightsOut(object):
    """Lights-Out solver."""
    
    def __init__(self, size=5):
        self.n = size
        self.base = lightsoutbase(self.n)
        self.invbase, self.null_vectors = GF2inv(self.base)
    
    def solve(self, b):
        b = np.asarray(b)
        assert b.shape[0] == b.shape[1] == self.n, "incompatible shape"
        
        if not self.issolvable(b):
            raise ValueError("The given setup is not solvable")
        
        # Find the base solution.
        first = np.dot(self.invbase, b.ravel()) & 1
        
        # Given a solution, we can find more valid solutions
        # adding any combination of the null vectors.
        # Find the solution with the minimum number of 1's.
        solutions = [(first + reduce(add, nvs, 0)) & 1 for nvs in powerset(self.null_vectors)]
        final = min(solutions, key=lambda x: x.sum())
        return np.reshape(final, (self.n, self.n))
    
    def issolvable(self, b):
        """Determine if the given configuration is solvable.
        
        A configuration is solvable if it is orthogonal to
        the null vectors of the base.
        """
        b = np.asarray(b)
        assert b.shape[0] == b.shape[1] == self.n, "incompatible shape"
        b = b.ravel()
        p = [np.dot(x, b) & 1 for x in self.null_vectors]
        return not any(p)
    

def main():
    """Example."""
    lo = LightsOut(5)
    b = np.array([[0, 0, 1, 0, 0],
                  [0, 1, 0, 1, 0],
                  [1, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 1]])
    bsol = lo.solve(b)
    print("The solution of\n{}\nis\n{}".format(b, bsol))


if __name__ == '__main__':
    main()

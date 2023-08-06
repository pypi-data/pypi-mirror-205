import cProfile
from random import seed, random, randint
import sys
from src.pyfloat import PyFloat

#!/usr/bin/env python
"""
    Copyright (C) 2020 __sh0l1n.
   
    Contributed by __sh0l1n <https://github.com/sh1l0n>, 2020.
    PyFloat is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    PyFloat Library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
    You should have received a copy of the GNU Lesser General Public
    License along with the PyFloat Library; if not, see
    <http://www.gnu.org/licenses/>. 
"""

from random import seed, random, randint
import sys
from src.pyfloat import PyFloat
import math

def sum(a, b):
    return a + b
def sumP(a, b):
    return PyFloat(a) + PyFloat(b)
def sub(a, b):
    return a - b
def subP(a, b):
    return PyFloat(a) - PyFloat(b)
def mul(a, b):
    return a * b
def mulP(a, b):
    return PyFloat(a) * PyFloat(b)

def profileInt(target):
    for i in range(0, 100000):
        a = randomInteger()
        b = randomInteger()
        target(a, b)

def profileFloat(target):
    for i in range(0, 100000):
        a = random()
        b = random()
        target(a, b)

def randomInteger(min=-sys.maxsize, max=sys.maxsize):
    return randint(min, max)

if __name__ == "__main__":
    seed(1)
    cProfile.run("profileInt(sum)")
    cProfile.run("profileInt(sumP)")
    cProfile.run("profileFloat(sum)")
    cProfile.run("profileFloat(sumP)")

    cProfile.run("profileInt(sub)")
    cProfile.run("profileInt(subP)")
    cProfile.run("profileFloat(sub)")
    cProfile.run("profileFloat(subP)")

    cProfile.run("profileInt(mul)")
    cProfile.run("profileInt(mulP)")
    cProfile.run("profileFloat(mul)")
    cProfile.run("profileFloat(mulP)")


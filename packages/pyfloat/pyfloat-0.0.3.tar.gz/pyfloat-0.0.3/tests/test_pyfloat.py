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


def testIntSum(i, j):
    target = PyFloat(i + j)
    value = PyFloat(i) + PyFloat(j)
    assert target == value, (str(i)  + " + " + str(j) + " should be " + str(target) + " and is " + str(value))

def testIntSub(i, j):
    target = PyFloat(i - j)
    value = PyFloat(i) - PyFloat(j)
    assert target == value, (str(i)  + " - " + str(j) + " should be " + str(target) + " and is " + str(value))

def testIntMul(i, j):
    target = PyFloat(i * j)
    value = PyFloat(i) * PyFloat(j)
    assert target == value, (str(i)  + " * " + str(j) + " should be " + str(target) + " and is " + str(value))

# def testIntPow(i, j):
#     target = str(pow(i,j))
#     iStr = str(i)
#     value = pyfloat.pow(iStr, j)
#     assert target == value, ("pow("+iStr  + ", " + str(j) + ") should be " + str(target) + " and is " + str(value))

def getDecimals(a):
    aS = a.split(".")
    return 0 if len(aS)==1 else len(aS[1])

def testIntSumDecimals(a, b, decimalsToCheck):
    value = PyFloat(a) + PyFloat(b)
    target = PyFloat(a + b)
    value = str(value)[0:decimalsToCheck]
    target = str(target)[0:decimalsToCheck]
    assert (value == target), ("Decimal -> " + str(a) + " + " + str(b) + " should be [" + target + "] and is [" +  value + "]")

def testIntSubDecimals(a, b, decimalsToCheck):
    value = PyFloat(a) - PyFloat(b)
    target = PyFloat(a - b)
    valueS = str(value)[0:decimalsToCheck]
    targetS = str(target)[0:decimalsToCheck]
    assert (valueS == targetS), ("Decimal -> " + str(a) + " - " + str(b) + " should be [" + target + "] and is [" +  value + "], valueS : " + valueS + " targetS " + targetS)

def testIntMulDecimals(a, b, decimalsToCheck):
    value = PyFloat(a) * PyFloat(b)
    target = PyFloat(a * b)
    value = str(value)[0:decimalsToCheck]
    target = str(target)[0:decimalsToCheck]
    assert (value == target), ("Decimal -> " + str(a) + " * " + str(b) + " should be [" + target + "] and is [" +  value + "]")

def testComparators(a, b):
    aPy, bPy = PyFloat(a), PyFloat(b)
    assert (a>b) == (aPy>bPy), ("Comparation (a>b) == (aPy>bPy) fails " + str(a) + " <--> " + str(b) )
    assert (a>=b) == (aPy>=bPy), ("Comparation (a>=b) == (aP>=bPy) fails " + str(a) + " <--> " + str(b) )
    assert (a==b) == (aPy==bPy), ("Comparation (a==b) == (aPy==bPy) fails " + str(a) + " <--> " + str(b) )
    assert (a!=b) == (aPy!=bPy), ("Comparation (a!=b) == (aPy!=bPy) fails " + str(a) + " <--> " + str(b) )
    assert (a<=b) == (aPy<=bPy), ("Comparation (a<=b) == (aPy<=bPy) fails " + str(a) + " <--> " + str(b) )
    assert (a<b) == (aPy<bPy), ("Comparation (a<b) == (aPy<bPy) fails " + str(a) + " <--> " + str(b) )
    
# def testIntDiv(i, j):
#     target = str(i / j)
#     iStr = str(i)
#     jStr = str(j)
#     value = div(iStr, jStr)
#     assert target == value, (iStr  + " / " + jStr + " should be " + str(target) + " and is " + str(value))

def randomInteger(min=-sys.maxsize, max=sys.maxsize):
    return randint(min, max)

if __name__ == "__main__":
    seed(1)

    decimalsToCheck = 6
    for i in range(0, 100000):
        a = randomInteger()
        b = randomInteger()
        ar = random()
        br = random()
        testIntSum(a, b)
        testIntSub(a, b)
        testIntMul(a, b)
        # testIntPow(a, randomInteger(0, 10))
        testIntSumDecimals(ar, br, decimalsToCheck)
        testIntSubDecimals(ar, br, decimalsToCheck)
        testIntMulDecimals(ar, br, decimalsToCheck)
        # testIntDiv(a, b)

        testComparators(a, b)
        

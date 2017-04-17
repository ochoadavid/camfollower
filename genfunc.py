#!/usr/bin/python3
# -*- coding: utf-8 -*-
## Autor: David Ochoa

import numpy as np

class Genfunc():
    """ Cam generation function Base class. As it, generates a constant velocity function.
    Parameters: theta_start: angle where this function should start.
                theta_end: ending angle of the function.
                h_start, h_end: starting and ending height, defaults to 0 and 1.
                ret: True if returning (fall) movement.
    """
    def __init__(self, theta_start, theta_end, h_start=0.0, h_end=1.0, ret=False):
        self.t_start = theta_start
        self.t_end = theta_end
        self.h_start = h_start
        self.h_end = h_end
        self.ret = ret

    def calcz(self, theta):
        """ Return a z (0-1) value given a theta value (or array of values). """
        num = theta - self.t_start
        den = self.t_end - self.t_start
        return num / den

    def calc(self, theta):
        """ Return the function value given a theta value. """
        z = self.calcz(theta)
        y = self.func(z)
        if self.ret:
            y = 1 - y
        return self.h_start + y * self.h_end

    def func(self, zeta):
        """ Generation function, f(z) = z. """
        return zeta

    def plotgen(self):
        """ Returns cartesian (x,y) arrays to plot the function. """
        x = np.arange(self.t_start, self.t_end)
        y = self.calc(x)
        return x,y

class Uniform(Genfunc):
    """ Dummy generation class using linear movement. """
    pass

class Armonic(Genfunc):
    """ Armonic movement function class. """
    def func(self, zeta):
        return 1/2 * (1 - np.cos(zeta * np.pi))

class Poly345(Genfunc):
    """ 3-4-5 polinomial movement function class. """
    def func(self, zeta):
        p = np.power
        return 10 * p(zeta,3) - 15 * p(zeta,4) + 6 * p(zeta,5)

class Poly4567(Genfunc):
    """ 4-5-6-7 polinomial movement function class. """
    def func(self, zeta):
        p = np.power
        return 35 * p(zeta,4) - 84 * p(zeta,5) + 70 * p(zeta,6) - 20 * p(zeta,7)

class Cycloidal(Genfunc):
    """ Cycloidal movement function class. """
    def func(self, zeta):
        return zeta - 1/(2*np.pi) * np.sin(2* zeta * np.pi)

class Parabolic(Genfunc):
    """ Double (simetric) parabolic movement function class. """
    def func(self, zeta):
        out = np.where(zeta < 0.5,
                       2 * zeta * zeta,
                       1 - 2 * (1 - zeta) * (1 - zeta))
        return out

class BottomDwell(Genfunc):
    """ Bottom dwell function class f(z) = 0.0. """
    def func(self, zeta):
        return np.zeros_like(zeta)

class TopDwell(Genfunc):
    """ Top dwell function class f(z) = h_end. """
    def func(self, zeta):
        return np.ones_like(zeta)

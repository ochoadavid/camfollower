#!/usr/bin/python3
# -*- coding: utf-8 -*-
## Autor: David Ochoa

import numpy as np

class GeneratorCil():
    """ Cam generation class with cilindrical follower. Creates a cam profile by "cutting" a blank.
    Parameters: prime_circle_radius, follower_radius, genfunc=[functions list]
                exentricity =
                resolution_deg = cam resolution (degrees)
                max_radius = blank disk radius
    """
    def __init__(self, prime_circle_radius, follower_radius, genfunc=[],
                        excentricity=0, resolution_deg=1.0, max_radius=10.0):
        self.rp = prime_circle_radius
        self.rf = follower_radius
        self.gflist = genfunc
        self.ex = excentricity
        self.res = resolution_deg
        self.reset(max_radius)

    def reset(self, r):
        """ (re)generate cam baseline and degree data. """
        self.theta = np.arange(0.0,360.0,self.res)
        self.values = np.ones_like(self.theta) * r

    def evaluate_gf(self, value):
        """ Evaluate cam height for a value using function list. """
        for gf in self.gflist:
            if value >= gf.t_start and value < gf.t_end:
                return gf.calc(value)
        raise ValueError("Generation functions did't define the whole circle")

    def center_pos(self, value):
        """ Calculate instantaneous follower position (x,y) given a value. """
        theta_excen = np.arctan2(self.ex, self.rp)
        h = self.evaluate_gf(value)
        value_rad = value * np.pi / 180
        xp = self.rp * np.cos(value_rad + theta_excen)
        yp = self.rp * np.sin(value_rad + theta_excen)
        xf = h * np.cos(value_rad)
        yf = h * np.sin(value_rad)
        return xp + xf, yp + yf

    def cam_cut(self, val):
        """ "Cuts" the cam blank for a given value (theta). """
        fcx, fcy = self.center_pos(val)
        fcircle = np.arange(0.0,360.0,1.0) * np.pi / 180
        fx = fcx + self.rf * np.cos(fcircle)
        fy = fcy + self.rf * np.sin(fcircle)
        theta = np.arctan2(fy, fx) * 180 / np.pi
        theta = np.where(theta < 0.0, theta+360, theta)
        dist = np.sqrt(fy * fy + fx * fx)
        for th, dt in zip(theta, dist):
            idx = (np.abs(self.theta-th)).argmin()
            self.values[idx] = np.min((self.values[idx], dt))

    def profile_gen(self):
        """ Calls cam_cut for every angle. """
        for i in np.arange(0.0, 360.0, 1.0):
            self.cam_cut(i)

    def xy_profile(self, rotate_angle=0.0):
        """ Outputs two numpy arrays with the x and y coordinates of the cam in a given angle. """
        theta_calc = (self.theta - rotate_angle) * np.pi / 180
        x = self.values * np.cos(theta_calc)
        y = self.values * np.sin(theta_calc)
        return x, y

    def xy_follower(self, val):
        """ Outputs two numpy arrays with the x and y coordinates of the follower for a given angle. """
        h = self.evaluate_gf(val)
        theta_excen = np.arctan2(self.ex, self.rp)
        fcx = self.rp * np.cos(theta_excen) + h
        fcy = self.ex
        fcircle = np.arange(0.0,360.0,1.0) * np.pi / 180
        fx = fcx + self.rf * np.cos(fcircle)
        fy = fcy + self.rf * np.sin(fcircle)
        return fx, fy

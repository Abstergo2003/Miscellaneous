import pygame as pg # type: ignore
import numpy as np
import math
from matrix_functions import *

#similar to camera but acts as light and is not controlable
class Light:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0]) # getting position
        # moving patterns
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.2
        self.rotation_speed = 0.005

    def loot_at_trans(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, -x],
            [0, 1, 0, -y],
            [0, 0, 1, -z],
            [0, 0, 0, 1]
        ])
    
    def loot_at_rot(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, -fx, 0],
            [ry, uy, -fy, 0],
            [rz, uz, -fz, 0],
            [0, 0, 0, 1]
        ])
    
    def light_look_at(self):
        return self.loot_at_trans() @ self.loot_at_rot()
import pygame as pg # type: ignore
import numpy as np
import math
from matrix_functions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0]) # getting position
        # moving patterns
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        # horizontal filed of view
        self.h_fov = math.pi / 3
        # vertical field of view
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        # near plane, far plane
        self.near_plane = 0.1
        self.far_plane = 100
        # transformations speed
        self.moving_speed = 0.2
        self.rotation_speed = 0.005

    # controls camera movement
    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed #move left
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed #move right
        if key[pg.K_q]:
            self.position += self.forward * self.moving_speed #move forward
        if key[pg.K_e]:
            self.position -= self.forward * self.moving_speed #move backwords
        if key[pg.K_w]:
            self.position += self.up * self.moving_speed #move uo
        if key[pg.K_s]:
            self.position -= self.up * self.moving_speed #move down
        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed) #rotate left
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed) #rotate right
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed) #rotate up
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed) #rotate down
        if key[pg.K_z]:
            self.camera_zaw(self.rotation_speed) #rotate counterclockwise
        if key[pg.K_x]:
            self.camera_zaw(-self.rotation_speed) #rotate clockwise

    #rotate camera by Y axis
    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    # rotate camera by X Axis
    def camera_pitch(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    # rotate camera by Z Axis
    def camera_zaw(self, angle):
        rotate = rotate_z(angle);
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    # helping matrix 
    def loot_at_trans(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, -x],
            [0, 1, 0, -y],
            [0, 0, 1, -z],
            [0, 0, 0, 1]
        ])
    
    # translation matrix
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    # helping matrix
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

    # rotation matrix
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    # gets camera matrix
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
    
    # gets helping matrix
    def look_at(self):
        return self.loot_at_trans() @ self.loot_at_rot()
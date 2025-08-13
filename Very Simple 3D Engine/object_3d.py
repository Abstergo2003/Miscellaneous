import pygame as pg # type: ignore
from matrix_functions import *
from numba import njit
import numpy as np

# convert to machine code to boost fps
@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(self, render, vertexes, faces):
        self.render = render
        self.vertexes = np.array(vertexes, dtype=np.float64) # Ensure vertexes are numpy arrays
        self.faces = faces # Convert faces to numpy array of integers
        self.z_order = np.zeros(len(self.faces))
        self.shaded_colors = [] # here colors are saved for shading
        self.shadow_map = None
        self.renderMesh = False # rendering mode

    # general method to draw
    def draw(self):
        if self.renderMesh:
            self.screen_projection_Full()
        else:
            self.screen_projection_mesh()

    # switches modes
    def projection_control(self):
            self.renderMesh = not self.renderMesh

    # draws fuul faces
    def screen_projection_Full(self):
        #sorts faces for painter algorithm
        self.sort()
        # obj vertexes to camera space
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        # vertexes to clip space
        vertexes = vertexes @ self.render.projection.projection_matrix
        # normalizing vertexes by w, and cuting when has values outside <-1,1>
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        
        # getting vertexes of light
        light_vertexes = vertexes @ self.render.light.light_look_at()
        # cutting off vertexes that are outside of screen with tolerancy for better effect
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        # adjust to scrren resolution
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        # choose cords for X, Y axis
        vertexes = vertexes[:, :2]
        light_vertexes /= light_vertexes[:, -1].reshape(-1, 1)
        light_vertexes = light_vertexes @ self.render.projection.to_screen_matrix
        light_vertexes = light_vertexes[:, :2]

        # draws in order
        for index in np.argsort(self.z_order):
            face = self.faces[index]
            polygon = vertexes[face]
            # gets color shade
            shaded_color = self.shaded_colors[index]
            r, g, b = shaded_color
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))

            # draw polygon
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, [r, g, b], polygon)

    # draws in mesh mode, more fps because no need for sorting and shading
    def screen_projection_mesh(self):
        # obj vertexes to camera space
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        # vertexes to clip space
        vertexes = vertexes @ self.render.projection.projection_matrix
        # normalizing vertexes by w, and cuting when has values outside <-1,1>
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        # generate shadow map
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        # adjust to scrren resolution
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        # choose cords for X, Y axis
        vertexes = vertexes[:, :2]

        #drawing faces
        for face in self.faces:
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, pg.Color("orange"), polygon, 1)


        #drawing vertexes
        for vertex in vertexes:
            if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.circle(self.render.screen, pg.Color("white"), vertex, 2)

    # self translation function
    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    # self scaling function
    def scale(self, n):
        self.vertexes = self.vertexes @ scale(n)
    
    # self rotation by X function
    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    # self rotation by Y function
    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    # self rotation by Z function
    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)

    # algorytm malarza
    def sort(self, light_dir=np.array([-5, 5, -50]), shade=np.array([50, 99, 168])):
        self.z_order = np.zeros(len(self.faces))
        self.shaded_colors = np.zeros((len(self.faces), 3))
        light_dir = light_dir / np.linalg.norm(light_dir)
        for i in range(len(self.faces)):
            face = self.faces[i]
            vertex = self.vertexes[face]
            vertex_3d = vertex[:, :3]
            camera_mat = self.render.camera.look_at()
            transformed_vertices = vertex @ camera_mat.T
            z_depths = [transformed_vertices[j, 2] for j in range(len(transformed_vertices))]
            self.z_order[i] = np.mean(z_depths)
            self.shaded_colors[i] = shadeV(vertex_3d, light_dir, shade)

# convert to machine code to boost fps
@njit
def shadeV(vertex_3d, light_dir, shade):
    edge1 = vertex_3d[1] - vertex_3d[0]
    edge2 = vertex_3d[2] - vertex_3d[0]
    face_normal = np.cross(edge1, edge2)
    face_normal = face_normal / np.linalg.norm(face_normal)
    intensity = max(np.dot(face_normal, light_dir), 0.3)
    return intensity * shade
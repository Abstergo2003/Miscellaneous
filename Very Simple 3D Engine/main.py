import pygame as pg
from camera import *
from projection import *
from object_3d import *
from light_camera import *
from force_obj import object_string

class SoftwareRender:
    # standard pygame attributes
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.z_buffer = np.full((self.WIDTH, self.HEIGHT), np.inf, dtype=np.float64)
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_object()

    #creates object
    def create_object(self):
        self.camera = Camera(self, [-5, 5, -50])
        self.light = Light(self, [-5, 5, -50])
        self.projection = Projection(self)
        self.object = self.get_object_from_file(object_string)

    # rendering method
    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.object.draw()

    # parses string to arrays to create object
    def get_object_from_file(self, o_str):
        vertex, faces = [], []
        for line in o_str.split('\n'):
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    # main loop
    def run(self):
        while True:
            self.draw()
            self.camera.control()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        # swithces beetween rendering mesh and rendering full faces
                        self.object.projection_control()
            mode = ""
            if not self.object.renderMesh:
                mode = "Mesh"
            else:
                mode = "Full"
            pg.display.set_caption(str(self.clock.get_fps()) + " FPS. To change mode click 'P'. Current mode: " + mode + ".") # displays FPS and render mode
            pg.display.flip() #updates screen
            self.clock.tick(self.FPS)

# runs app if this is main file (not name but was called from console using "python fileneame.py")
if __name__ == "__main__":
    app = SoftwareRender()
    app.run()
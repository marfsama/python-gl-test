
'''
use pyshaders for compiling shaders and setting uniforms
23.03. 10:35 Uhr
'''

from pyglet.gl import *
from euclid import *

import pyshaders

from torus import Torus

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4, 
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)


def update(dt):
    global rx, ry, rz
    rx += dt * 1
    ry += dt * 80
    rz += dt * 30
    rx %= 360
    ry %= 360
    rz %= 360


pyglet.clock.schedule(update)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.use()

    matrix = model_matrix()
    shader.uniforms.ModelMatrix = [matrix]

    projection = Matrix4.new_perspective(math.radians(60.), window.width / float(window.height), .1, 1000)
    shader.uniforms.ProjectionMatrix = [projection]

    batch.draw()


def model_matrix():
    quaternion = Quaternion.new_rotate_euler(math.radians(rx), math.radians(ry), math.radians(rz))
    rotation = quaternion.get_matrix()
    translation = Matrix4.new_translate(0.0, 0.0, -4.0)
    matrix = translation * rotation
    return matrix


# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)


def read_file(filename):
    with open(filename, 'r') as content_file:
        return content_file.read()


def load_program():
    return pyshaders.from_string(read_file("shader03.vert"), [])


def setup():
    # One-time GL setup
    pyshaders.transpose_matrices(False)

    glClearColor(1, 1, 1, 1)
    glColor3f(1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    return load_program()


shader = setup()
print("shader: ", shader)
batch = pyglet.graphics.Batch()
torus = Torus(1, 0.3, 50, 30)
torus.add_to_batch(batch)
rx = ry = rz = 0



pyglet.app.run()

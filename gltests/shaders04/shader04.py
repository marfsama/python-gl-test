
'''
simple lightning with vertex shader
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


# a b c d
# e f g h
# i j k l
# m n o p

def get_normal_matrix(matrix):
    normal_matrix = Matrix3.new_identity()
    normal_matrix[:] = (matrix.a, matrix.b, matrix.c,
                        matrix.e, matrix.f, matrix.g,
                        matrix.i, matrix.j, matrix.k
                        )
    return normal_matrix


@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)

    glViewport(0, 0, width, height)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shader.use()

    matrix = model_matrix()
    normal_matrix = get_normal_matrix(matrix)
    projection = Matrix4.new_perspective(math.radians(60.), window.width / float(window.height), .1, 1000)
    shader.uniforms.ProjectionMatrix = [projection]
    shader.uniforms.ModelMatrix = [matrix]

    glViewport(0, 0, window.width//2, window.height//2)
    shader.uniforms.NormalMatrix = [normal_matrix.transposed()]
    batch.draw()

    glViewport(window.width//2, 0, window.width//2, window.height//2)
    shader.uniforms.NormalMatrix = [normal_matrix.inverse()]
    batch.draw()

    glViewport(window.width//2, window.height//2, window.width//2, window.height//2)
    shader.uniforms.NormalMatrix = [Matrix3.new_identity()]
    batch.draw()

    shader.clear()
    glViewport(0, window.height//2, window.width//2, window.height//2)
    glLoadIdentity()
    glTranslatef(0, 0, -4)
    glRotatef(rz, 0, 0, 1)
    glRotatef(ry, 0, 1, 0)

    batch.draw()

def model_matrix():
    quaternion = Quaternion.new_rotate_euler(0, math.radians(rz), 0) * \
                Quaternion.new_rotate_euler(math.radians(ry), 0, 0)
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
    return pyshaders.from_string(read_file("shader04.vert"), [])


def setup():
    pyshaders.transpose_matrices(False)
    # One-time GL setup
    glClearColor(1, 1, 1, 1)
    glColor3f(1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    return load_program()


shader = setup()
print("shader: ", shader)
batch = pyglet.graphics.Batch()
torus = Torus(1, 0.3, 50, 30)
torus.add_to_batch(batch)
rx = ry = rz = 0

pyglet.app.run()

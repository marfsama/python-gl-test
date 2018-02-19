
'''
generate model transform matrix. use these in the vertex shader.
'''

from pyglet.gl import *
from euclid import *

from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GL import glGetProgramInfoLog

from torus import Torus
from ctypes import *

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4, 
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


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
    glLoadIdentity()

    quaternion = Quaternion.new_rotate_euler(math.radians(rx), math.radians(ry), math.radians(rz))
    rotation = quaternion.get_matrix()
    translation = Matrix4.new_translate(0.0, 0.0, -4.0)
    matrix = translation * rotation
    location = glGetUniformLocation(program, b"ModelMatrix")
    glUniformMatrix4fv(location, 1, 0, (GLfloat * 16)(*matrix))

    projection = Matrix4.new_perspective (math.radians(60.), window.width / float(window.height), .1, 1000)
    location = glGetUniformLocation(program, b"ProjectionMatrix")
    glUniformMatrix4fv(location, 1, 0, (GLfloat * 16)(*projection))


    batch.draw()


# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)


def read_file(filename):
    with open(filename, 'r') as content_file:
        return content_file.read()


def load_program():
    vertex_shader_source = read_file("shader02.vert")

    vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)

    program = compileProgram(vertex_shader)

    print("program info log", glGetProgramInfoLog(program))


    glUseProgram(program)

    return program


def setup():
    # One-time GL setup
    glClearColor(1, 1, 1, 1)
    glColor3f(1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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


program = setup()
print("program: ", program)
batch = pyglet.graphics.Batch()
torus = Torus(1, 0.3, 50, 30)
torus.add_to_batch(batch)
rx = ry = rz = 0



pyglet.app.run()

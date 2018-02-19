
'''Displays a rotating torus using the pyglet.graphics API.

This example is very similar to examples/opengl.py, but uses the
pyglet.graphics API to construct the indexed vertex arrays instead of
using OpenGL calls explicitly.  This has the advantage that VBOs will
be used on supporting hardware automatically.  

The vertex list is added to a batch, allowing it to be easily rendered
alongside other vertex lists with minimal overhead.
'''

from pyglet.gl import *

from node import *
from torus import Torus

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
    viewport0[0], viewport0[1], viewport0[2], viewport0[3] = 0, 0, width, height
    viewport1[0], viewport1[1], viewport1[2], viewport1[3] = 0, 0, width // 2, height // 2
    viewport2[0], viewport2[1], viewport2[2], viewport2[3] = 0, height // 2, width // 2, height // 2
    viewport3[0], viewport3[1], viewport3[2], viewport3[3] = width // 2, 0, width // 2, height // 2
    viewport4[0], viewport4[1], viewport4[2], viewport4[3] = width // 2, height // 2, width // 2, height // 2
    glViewport(0, 0, width, height)
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
    glTranslatef(0, 0, -4)
    glRotatef(rz, 0, 0, 1)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rx, 1, 0, 0)

    batch.draw()

#    label.draw()

def setup():
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

    # Define a simple function to create ctypes arrays of floats:
    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)


setup()
batch = pyglet.graphics.Batch()
torus = Torus(1, 0.3, 50, 30)
viewport0 = [0, 0, 640, 480]
viewport1 = [0, 0, 320, 240]
viewport2 = [0  , 240, 320, 240]
viewport3 = [320, 0,   320, 240]
viewport4 = [320, 240, 320, 240]

perspectiveGroup = PerspectiveGroup(None)

torus.add_to_batch(batch=batch, group=ViewportGroup(viewport1, perspectiveGroup))
torus.add_to_batch(batch=batch, group=ViewportGroup(viewport2, perspectiveGroup))
torus.add_to_batch(batch=batch, group=ViewportGroup(viewport3, perspectiveGroup))
torus.add_to_batch(batch=batch, group=ViewportGroup(viewport4, perspectiveGroup))
rx = ry = rz = 0

guiGroup = GUIProjectionGroup()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center',
                          group=guiGroup,
                          batch=batch)

pyglet.app.run()

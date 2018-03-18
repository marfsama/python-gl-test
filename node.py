from pyglet.gl import *
import pyglet
from tests.extlibs.mock import self

from euclid import *


class ViewportGroup(pyglet.graphics.Group):
    """
    Sets the viewport upon entering the group.

    """
    def __init__(self, viewport, parent=None):
        super(ViewportGroup, self).__init__(parent)
        self.viewport = viewport
        self.old_viewport = None

    def set_state(self):
        self.old_viewport = (GLint * 4)()
        glGetIntegerv(GL_VIEWPORT, self.old_viewport)
        glViewport(*self.viewport)
        print("set viewport to ", *self.viewport)

    def unset_state(self):
        if self.old_viewport is not None:
            glViewport(*self.old_viewport)
            print("reset viewport to ", *self.old_viewport)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.viewport)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.viewport == other.viewport)

    def __hash__(self):
        return hash((id(self.parent), *self.viewport))


class PerspectiveGroup(pyglet.graphics.OrderedGroup):
    """
    Sets a perspective projection.
    https://www.khronos.org/opengl/wiki/GluPerspective_code

    """

    def __init__(self, dimensions=None, near=.1, far=1000., parent=None):
        super(PerspectiveGroup, self).__init__(0, parent)
        self.near = near
        self.far = far
        self.dimensions = dimensions

    def set_state(self):
        if self.dimensions is None:
            viewport = (GLint * 4)()
            glGetIntegerv(GL_VIEWPORT, viewport)
            _, _, width, height = viewport
        else:
            width, height = self.dimensions[::2]

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
        print("set perspective projection")

    def unset_state(self):
        # no reseting the projection matrix.
        pass

    def __repr__(self):
        return '%s(%r - %r)' % (self.__class__.__name__, self.near, self.far)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.dimensions == other.dimensions and
                self.near == other.near and
                self.far == other.far)

    def __hash__(self):
        return hash((id(self.parent), self.near, self.far, self.dimensions))


class GUIProjectionGroup(pyglet.graphics.OrderedGroup):
    """
    Sets the projection matrix for GUI elements (orthogonal).
    Additionally the depth buffer and face culling is disabled.

    """

    def __init__(self, dimensions=None, parent=None):
        super(GUIProjectionGroup, self).__init__(100, parent)
        self.dimensions = dimensions

    def set_state(self):
        if self.dimensions is None:
            viewport = (GLint * 4)()
            glGetIntegerv(GL_VIEWPORT, viewport)
            _, _, width, height = viewport
        else:
            width, height = self.dimensions[::2]

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        print("set ortho projection to ", width, "x", height)

    def unset_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.dimensions)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.dimensions == other.dimensions)

    def __hash__(self):
        return hash((id(self.parent), self.dimensions))


class TransformGroup(pyglet.graphics.Group):
    def __init__(self, translation=Vector3(0., 0., 0.), rotation=Quaternion(), scale=Vector3(1., 1., 1.), parent=None):
        super(TransformGroup, self).__init__(parent)
        self.translation = translation
        self.rotation = rotation
        self.scale = scale

    def set_state(self):
        glPushMatrix()
        matrix = Matrix4.new_translate(self.translation.x, self.translation.y, self.translation.z)
        matrix *= self.rotation.get_matrix()
        matrix *= Matrix4.new_scale(self.scale.x, self.scale.y, self.scale.z)
        buffer = (GLfloat * 16)()

        glMultMatrixf(buffer)

    def unset_state(self):
        glPopMatrix()

    def __eq__(self, other):
        # TransformGroups change during their lifetime, so it cannot be cached or merged with
        # another one.
        return other is self

    def __hash__(self):
        return hash((id(self)))

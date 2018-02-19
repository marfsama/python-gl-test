#!/usr/bin/env python
#
# euclid graphics maths module
#
# Copyright (c) 2006 Alex Holkner
# Alex.Holkner@mail.google.com
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

# changes
# 01.02.2018 - marfsama - added python3 compability, removed stuff not needed

"""euclid graphics maths module

Documentation and tests are included in the file "euclid.txt", or online
at http://code.google.com/p/pyeuclid
"""

__docformat__ = 'restructuredtext'
__version__ = '$Id$'
__revision__ = '$Revision$'

import math
import operator
import types

# Some magic here.  If _use_slots is True, the classes will derive from
# object and will define a __slots__ class variable.  If _use_slots is
# False, classes will be old-style and will not define __slots__.
#
# _use_slots = True:   Memory efficient, probably faster in future versions
#                      of Python, "better".
# _use_slots = False:  Ordinary classes, much faster than slots in current
#                      versions of Python (2.4 and 2.5).
_use_slots = True

# Implement _use_slots magic.
class _EuclidMetaclass(type):
    def __new__(mcs, name, bases, dct):
        if '__slots__' in dct:
            dct['__getstate__'] = mcs._create_getstate(dct['__slots__'])
            dct['__setstate__'] = mcs._create_setstate(dct['__slots__'])
        if _use_slots:
            return type.__new__(mcs, name, bases + (object,), dct)
        else:
            if '__slots__' in dct:
                del dct['__slots__']
            return types.ClassType.__new__(type, name, bases, dct)

    @classmethod
    def _create_getstate(mcs, slots):
        def __getstate__(self):
            d = {}
            for slot in slots:
                d[slot] = getattr(self, slot)
            return d

        return __getstate__

    @classmethod
    def _create_setstate(mcs, slots):
        def __setstate__(self, state):
            for name, value in list(state.items()):
                setattr(self, name, value)

        return __setstate__


__metaclass__ = _EuclidMetaclass


class Vector3:
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __copy__(self):
        return self.__class__(self.x, self.y, self.z)

    copy = __copy__

    def __repr__(self):
        return 'Vector3(%.2f, %.2f, %.2f)' % (self.x,
                                              self.y,
                                              self.z)

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and \
                   self.y == other.y and \
                   self.z == other.z
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return self.x == other[0] and \
                   self.y == other[1] and \
                   self.z == other[2]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return self.x != 0 or self.y != 0 or self.z != 0

    def __len__(self):
        return 3

    def __getitem__(self, key):
        return (self.x, self.y, self.z)[key]

    def __setitem__(self, key, value):
        temp = [self.x, self.y, self.z]
        temp[key] = value
        self.x, self.y, self.z = temp

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y, self.z)['xyz'.index(c)]
                          for c in name])
        except ValueError:
            raise AttributeError(name)

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return Vector3(self.x + other[0],
                           self.y + other[1],
                           self.z + other[2])

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        else:
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        return self

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x,
                           self.y - other.y,
                           self.z - other.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return Vector3(self.x - other[0],
                           self.y - other[1],
                           self.z - other[2])

    def __rsub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(other.x - self.x,
                           other.y - self.y,
                           other.z - self.z)
        else:
            assert hasattr(other, '__len__') and len(other) == 3
            return Vector3(other.x - self[0],
                           other.y - self[1],
                           other.z - self[2])

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x,
                           self.y * other.y,
                           self.z * other.z)
        else:
            assert type(other) in (int, float)
            return Vector3(self.x * other,
                           self.y * other,
                           self.z * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        assert type(other) in (int, float)
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __floordiv__(self, other):
        assert type(other) in (int, float)
        return Vector3(operator.floordiv(self.x, other),
                       operator.floordiv(self.y, other),
                       operator.floordiv(self.z, other))

    def __rfloordiv__(self, other):
        assert type(other) in (int, float)
        return Vector3(operator.floordiv(other, self.x),
                       operator.floordiv(other, self.y),
                       operator.floordiv(other, self.z))

    def __truediv__(self, other):
        assert type(other) in (int, float)
        return Vector3(operator.truediv(self.x, other),
                       operator.truediv(self.y, other),
                       operator.truediv(self.z, other))

    def __rtruediv__(self, other):
        assert type(other) in (int, float)
        return Vector3(operator.truediv(other, self.x),
                       operator.truediv(other, self.y),
                       operator.truediv(other, self.z))

    def __neg__(self):
        return Vector3(-self.x,
                       -self.y,
                       -self.z)

    __pos__ = __copy__

    def __abs__(self):
        return math.sqrt(self.x ** 2 +
                         self.y ** 2 +
                         self.z ** 2)

    magnitude = __abs__

    def magnitude_squared(self):
        return self.x ** 2 + \
               self.y ** 2 + \
               self.z ** 2

    def normalize(self):
        d = self.magnitude()
        if d:
            self.x /= d
            self.y /= d
            self.z /= d
        return self

    def normalized(self):
        d = self.magnitude()
        if d:
            return Vector3(self.x / d,
                           self.y / d,
                           self.z / d)
        return self.copy()

    def dot(self, other):
        assert isinstance(other, Vector3)
        return self.x * other.x + \
               self.y * other.y + \
               self.z * other.z

    def cross(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.y * other.z - self.z * other.y,
                       -self.x * other.z + self.z * other.x,
                       self.x * other.y - self.y * other.x)

    def reflect(self, normal):
        # assume normal is normalized
        assert isinstance(normal, Vector3)
        d = 2 * (self.x * normal.x + self.y * normal.y + self.z * normal.z)
        return Vector3(self.x - d * normal.x,
                       self.y - d * normal.y,
                       self.z - d * normal.z)


class Matrix4:
    """
 a b c d
 e f g h
 i j k l
 m n o p

    """
    __slots__ = list("abcdefghijklmnop")

    def __init__(self):
        self.identity()

    def __copy__(self):
        m = Matrix4()
        m.a = self.a
        m.b = self.b
        m.c = self.c
        m.d = self.d
        m.e = self.e
        m.f = self.f
        m.g = self.g
        m.h = self.h
        m.i = self.i
        m.j = self.j
        m.k = self.k
        m.l = self.l
        m.m = self.m
        m.n = self.n
        m.o = self.o
        m.p = self.p
        return m

    copy = __copy__

    def __repr__(self):
        return ('Matrix4([% 8.2f % 8.2f % 8.2f % 8.2f\n'
                '         % 8.2f % 8.2f % 8.2f % 8.2f\n'
                '         % 8.2f % 8.2f % 8.2f % 8.2f\n'
                '         % 8.2f % 8.2f % 8.2f % 8.2f])') \
               % (self.a, self.b, self.c, self.d,
                  self.e, self.f, self.g, self.h,
                  self.i, self.j, self.k, self.l,
                  self.m, self.n, self.o, self.p)

    def __getitem__(self, key):
        return [self.a, self.e, self.i, self.m,
                self.b, self.f, self.j, self.n,
                self.c, self.g, self.k, self.o,
                self.d, self.h, self.l, self.p][key]

    def __setitem__(self, key, value):
        assert not isinstance(key, slice) or \
               key.stop - key.start == len(value), 'key length != value length'
        temp = self[:]
        temp[key] = value
        (self.a, self.e, self.i, self.m,
         self.b, self.f, self.j, self.n,
         self.c, self.g, self.k, self.o,
         self.d, self.h, self.l, self.p) = temp

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            # Cache attributes in local vars (see Matrix3.__mul__).
            sa = self.a
            sb = self.b
            sc = self.c
            sd = self.d
            se = self.e
            sf = self.f
            sg = self.g
            sh = self.h
            si = self.i
            sj = self.j
            sk = self.k
            sl = self.l
            sm = self.m
            sn = self.n
            so = self.o
            sp = self.p
            oa = other.a
            ob = other.b
            oc = other.c
            od = other.d
            oe = other.e
            of = other.f
            og = other.g
            oh = other.h
            oi = other.i
            oj = other.j
            ok = other.k
            ol = other.l
            om = other.m
            on = other.n
            oo = other.o
            op = other.p
            c = Matrix4()
            c.a = sa * oa + sb * oe + sc * oi + sd * om
            c.b = sa * ob + sb * of + sc * oj + sd * on
            c.c = sa * oc + sb * og + sc * ok + sd * oo
            c.d = sa * od + sb * oh + sc * ol + sd * op
            c.e = se * oa + sf * oe + sg * oi + sh * om
            c.f = se * ob + sf * of + sg * oj + sh * on
            c.g = se * oc + sf * og + sg * ok + sh * oo
            c.h = se * od + sf * oh + sg * ol + sh * op
            c.i = si * oa + sj * oe + sk * oi + sl * om
            c.j = si * ob + sj * of + sk * oj + sl * on
            c.k = si * oc + sj * og + sk * ok + sl * oo
            c.l = si * od + sj * oh + sk * ol + sl * op
            c.m = sm * oa + sn * oe + so * oi + sp * om
            c.n = sm * ob + sn * of + so * oj + sp * on
            c.o = sm * oc + sn * og + so * ok + sp * oo
            c.p = sm * od + sn * oh + so * ol + sp * op
            return c
        elif isinstance(other, Vector3):
            a = self
            b = other
            v = Vector3(0, 0, 0)
            v.x = a.a * b.x + a.b * b.y + a.c * b.z
            v.y = a.e * b.x + a.f * b.y + a.g * b.z
            v.z = a.i * b.x + a.j * b.y + a.k * b.z
            return v
        else:
            other = other.copy()
            other._apply_transform(self)
            return other

    def __imul__(self, other):
        assert isinstance(other, Matrix4)
        # Cache attributes in local vars (see Matrix3.__mul__).
        sa = self.a
        sb = self.b
        sc = self.c
        sd = self.d
        se = self.e
        sf = self.f
        sg = self.g
        sh = self.h
        si = self.i
        sj = self.j
        sk = self.k
        sl = self.l
        sm = self.m
        sn = self.n
        so = self.o
        sp = self.p
        oa = other.a
        ob = other.b
        oc = other.c
        od = other.d
        oe = other.e
        of = other.f
        og = other.g
        oh = other.h
        oi = other.i
        oj = other.j
        ok = other.k
        ol = other.l
        om = other.m
        on = other.n
        oo = other.o
        op = other.p
        self.a = sa * oa + sb * oe + sc * oi + sd * om
        self.b = sa * ob + sb * of + sc * oj + sd * on
        self.c = sa * oc + sb * og + sc * ok + sd * oo
        self.d = sa * od + sb * oh + sc * ol + sd * op
        self.e = se * oa + sf * oe + sg * oi + sh * om
        self.f = se * ob + sf * of + sg * oj + sh * on
        self.g = se * oc + sf * og + sg * ok + sh * oo
        self.h = se * od + sf * oh + sg * ol + sh * op
        self.i = si * oa + sj * oe + sk * oi + sl * om
        self.j = si * ob + sj * of + sk * oj + sl * on
        self.k = si * oc + sj * og + sk * ok + sl * oo
        self.l = si * od + sj * oh + sk * ol + sl * op
        self.m = sm * oa + sn * oe + so * oi + sp * om
        self.n = sm * ob + sn * of + so * oj + sp * on
        self.o = sm * oc + sn * og + so * ok + sp * oo
        self.p = sm * od + sn * oh + so * ol + sp * op
        return self

    def identity(self):
        self.a = self.f = self.k = self.p = 1.
        self.b = self.c = self.d = self.e = self.g = self.h = \
            self.i = self.j = self.l = self.m = self.n = self.o = 0.0
        return self

    def scale(self, x, y, z):
        result = self * Matrix4.new_scale(x, y, z)
        return result

    def translate(self, x, y, z):
        result = self * Matrix4.new_translate(x, y, z)
        return result

    def rotatex(self, angle):
        result = self * Matrix4.new_rotatex(angle)
        return result

    def rotatey(self, angle):
        result = self * Matrix4.new_rotatey(angle)
        return result

    def rotatez(self, angle):
        result = self * Matrix4.new_rotatez(angle)
        return result

    def rotate_axis(self, angle, axis):
        result = self * Matrix4.new_rotate_axis(angle, axis)
        return result

    def rotate_euler(self, heading, attitude, bank):
        result = self * Matrix4.new_rotate_euler(heading, attitude, bank)
        return result

    # Static constructors
    @classmethod
    def new_identity(cls):
        self = cls()
        return self

    @classmethod
    def new_scale(cls, x, y, z):
        self = cls()
        self.a = x
        self.f = y
        self.k = z
        return self

    @classmethod
    def new_translate(cls, x, y, z):
        self = cls()
        self.d = x
        self.h = y
        self.l = z
        return self

    @classmethod
    def new_rotatex(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self.f = self.k = c
        self.g = -s
        self.j = s
        return self

    @classmethod
    def new_rotatey(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self.a = self.k = c
        self.c = s
        self.i = -s
        return self

    @classmethod
    def new_rotatez(cls, angle):
        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        self.a = self.f = c
        self.b = -s
        self.e = s
        return self

    @classmethod
    def new_rotate_axis(cls, angle, axis):
        assert (isinstance(axis, Vector3))
        vector = axis.normalized()
        x = vector.x
        y = vector.y
        z = vector.z

        self = cls()
        s = math.sin(angle)
        c = math.cos(angle)
        c1 = 1. - c

        # from the glRotate man page
        self.a = x * x * c1 + c
        self.b = x * y * c1 - z * s
        self.c = x * z * c1 + y * s
        self.e = y * x * c1 + z * s
        self.f = y * y * c1 + c
        self.g = y * z * c1 - x * s
        self.i = x * z * c1 - y * s
        self.j = y * z * c1 + x * s
        self.k = z * z * c1 + c
        return self

    @classmethod
    def new_rotate_euler(cls, heading, attitude, bank):
        # from http://www.euclideanspace.com/
        ch = math.cos(heading)
        sh = math.sin(heading)
        ca = math.cos(attitude)
        sa = math.sin(attitude)
        cb = math.cos(bank)
        sb = math.sin(bank)

        self = cls()
        self.a = ch * ca
        self.b = sh * sb - ch * sa * cb
        self.c = ch * sa * sb + sh * cb
        self.e = sa
        self.f = ca * cb
        self.g = -ca * sb
        self.i = -sh * ca
        self.j = sh * sa * cb + ch * sb
        self.k = -sh * sa * sb + ch * cb
        return self

    @classmethod
    def new_perspective(cls, fov_y, aspect, near, far):
        # from the gluPerspective man page
        f = 1 / math.tan(fov_y / 2)
        self = cls()
        assert near != 0.0 and near != far
        self.a = f / aspect
        self.f = f
        self.k = (far + near) / (near - far)
        self.l = 2 * far * near / (near - far)
        self.o = -1
        self.p = 0
        return self


class Quaternion:
    # All methods and naming conventions based off
    # http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions

    # w is the real part, (x, y, z) are the imaginary parts
    __slots__ = ['w', 'x', 'y', 'z']

    def __init__(self):
        self.identity()

    def __copy__(self):
        q = Quaternion()
        q.w = self.w
        q.x = self.x
        q.y = self.y
        q.z = self.z

    copy = __copy__

    def __repr__(self):
        return 'Quaternion(real=%.2f, imag=<%.2f, %.2f, %.2f>)' % \
               (self.w, self.x, self.y, self.z)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            ax = self.x
            ay = self.y
            az = self.z
            aw = self.w
            bx = other.x
            by = other.y
            bz = other.z
            bw = other.w
            q = Quaternion()
            q.x = ax * bw + ay * bz - az * by + aw * bx
            q.y = -ax * bz + ay * bw + az * bx + aw * by
            q.z = ax * by - ay * bx + az * bw + aw * bz
            q.w = -ax * bx - ay * by - az * bz + aw * bw
            return q
        elif isinstance(other, Vector3):
            w = self.w
            x = self.x
            y = self.y
            z = self.z
            vx = other.x
            vy = other.y
            vz = other.z
            return Vector3(
                w * w * vx + 2 * y * w * vz - 2 * z * w * vy +
                x * x * vx + 2 * y * x * vy + 2 * z * x * vz -
                z * z * vx - y * y * vx,
                2 * x * y * vx + y * y * vy + 2 * z * y * vz +
                2 * w * z * vx - z * z * vy + w * w * vy -
                2 * x * w * vz - x * x * vy,
                2 * x * z * vx + 2 * y * z * vy +
                z * z * vz - 2 * w * y * vx - y * y * vz +
                2 * w * x * vy - x * x * vz + w * w * vz)
        else:
            other = other.copy()
            other._apply_transform(self)
            return other

    def __imul__(self, other):
        assert isinstance(other, Quaternion)
        ax = self.x
        ay = self.y
        az = self.z
        aw = self.w
        bx = other.x
        by = other.y
        bz = other.z
        bw = other.w
        self.x = ax * bw + ay * bz - az * by + aw * bx
        self.y = -ax * bz + ay * bw + az * bx + aw * by
        self.z = ax * by - ay * bx + az * bw + aw * bz
        self.w = -ax * bx - ay * by - az * bz + aw * bw
        return self

    def __abs__(self):
        return math.sqrt(self.w ** 2 +
                         self.x ** 2 +
                         self.y ** 2 +
                         self.z ** 2)

    magnitude = __abs__

    def magnitude_squared(self):
        return self.w ** 2 + \
               self.x ** 2 + \
               self.y ** 2 + \
               self.z ** 2

    def identity(self):
        self.w = 1
        self.x = 0
        self.y = 0
        self.z = 0
        return self

    def rotate_axis(self, angle, axis):
        result = self * Quaternion.new_rotate_axis(angle, axis)
        return result

    def rotate_euler(self, heading, attitude, bank):
        result = self * Quaternion.new_rotate_euler(heading, attitude, bank)
        return result

    def conjugated(self):
        q = Quaternion()
        q.w = self.w
        q.x = -self.x
        q.y = -self.y
        q.z = -self.z
        return q

    def normalize(self):
        d = self.magnitude()
        if d != 0:
            self.w /= d
            self.x /= d
            self.y /= d
            self.z /= d
        return self

    def normalized(self):
        d = self.magnitude()
        if d != 0:
            q = Quaternion()
            q.w /= d
            q.x /= d
            q.y /= d
            q.z /= d
            return q
        else:
            return self.copy()

    def get_angle_axis(self):
        q = self
        if q.w > 1:
            q = q.normalized()
        angle = 2 * math.acos(q.w)
        s = math.sqrt(1 - q.w ** 2)
        if s < 0.001:
            return angle, Vector3(1, 0, 0)
        else:
            return angle, Vector3(q.x / s, q.y / s, q.z / s)

    def get_euler(self):
        t = self.x * self.y + self.z * self.w
        if t > 0.4999:
            heading = 2 * math.atan2(self.x, self.w)
            attitude = math.pi / 2
            bank = 0
        elif t < -0.4999:
            heading = -2 * math.atan2(self.x, self.w)
            attitude = -math.pi / 2
            bank = 0
        else:
            sqx = self.x ** 2
            sqy = self.y ** 2
            sqz = self.z ** 2
            heading = math.atan2(2 * self.y * self.w - 2 * self.x * self.z,
                                 1 - 2 * sqy - 2 * sqz)
            attitude = math.asin(2 * t)
            bank = math.atan2(2 * self.x * self.w - 2 * self.y * self.z,
                              1 - 2 * sqx - 2 * sqz)
        return heading, attitude, bank

    def get_matrix(self):
        xx = self.x ** 2
        xy = self.x * self.y
        xz = self.x * self.z
        xw = self.x * self.w
        yy = self.y ** 2
        yz = self.y * self.z
        yw = self.y * self.w
        zz = self.z ** 2
        zw = self.z * self.w
        m = Matrix4()
        m.a = 1 - 2 * (yy + zz)
        m.b = 2 * (xy - zw)
        m.c = 2 * (xz + yw)
        m.e = 2 * (xy + zw)
        m.f = 1 - 2 * (xx + zz)
        m.g = 2 * (yz - xw)
        m.i = 2 * (xz - yw)
        m.j = 2 * (yz + xw)
        m.k = 1 - 2 * (xx + yy)
        return m

    # Static constructors
    @classmethod
    def new_identity(cls):
        return cls()

    @classmethod
    def new_rotate_axis(cls, angle, axis):
        assert (isinstance(axis, Vector3))
        axis = axis.normalized()
        s = math.sin(angle / 2)
        q = cls()
        q.w = math.cos(angle / 2)
        q.x = axis.x * s
        q.y = axis.y * s
        q.z = axis.z * s
        return q

    @classmethod
    def new_rotate_euler(cls, heading, attitude, bank):
        q = cls()
        c1 = math.cos(heading / 2)
        s1 = math.sin(heading / 2)
        c2 = math.cos(attitude / 2)
        s2 = math.sin(attitude / 2)
        c3 = math.cos(bank / 2)
        s3 = math.sin(bank / 2)

        q.w = c1 * c2 * c3 - s1 * s2 * s3
        q.x = s1 * s2 * c3 + c1 * c2 * s3
        q.y = s1 * c2 * c3 + c1 * s2 * s3
        q.z = c1 * s2 * c3 - s1 * c2 * s3
        return q

    @classmethod
    def new_interpolate(cls, q1, q2, t):
        assert isinstance(q1, Quaternion) and isinstance(q2, Quaternion)
        q = cls()

        cos_theta = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z
        theta = math.acos(cos_theta)
        if abs(theta) < 0.01:
            q.w = q2.w
            q.x = q2.x
            q.y = q2.y
            q.z = q2.z
            return q

        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        if abs(sin_theta) < 0.01:
            q.w = (q1.w + q2.w) * 0.5
            q.x = (q1.x + q2.x) * 0.5
            q.y = (q1.y + q2.y) * 0.5
            q.z = (q1.z + q2.z) * 0.5
            return q

        ratio1 = math.sin((1 - t) * theta) / sin_theta
        ratio2 = math.sin(t * theta) / sin_theta

        q.w = q1.w * ratio1 + q2.w * ratio2
        q.x = q1.x * ratio1 + q2.x * ratio2
        q.y = q1.y * ratio1 + q2.y * ratio2
        q.z = q1.z * ratio1 + q2.z * ratio2
        return q

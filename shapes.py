"""Basic shapes used to build the robot, the helicopter and the world.

Every shape is drawn around the current position, so you place it with
glTranslatef / glRotatef before calling it.
"""
from OpenGL.GL import (
    GL_QUADS, GL_TEXTURE_2D, glBegin, glBindTexture, glColor3f, glDisable, glEnable,
    glEnd, glNormal3f, glPopMatrix, glPushMatrix, glRotatef, glTexCoord2f, glTranslatef, glVertex3f,
)
from OpenGL.GLU import gluCylinder, gluDisk, gluNewQuadric, gluQuadricNormals, gluQuadricTexture, gluSphere, GLU_SMOOTH

_quadric = None


def quadric():
    """GLU 'quadric' object - GLU uses it to draw spheres, cylinders and disks."""
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricNormals(_quadric, GLU_SMOOTH)  # normals for lighting
        gluQuadricTexture(_quadric, True)        # texture coordinates
    return _quadric


def use_texture(texture_id, color=(1.0, 1.0, 1.0)):
    """Select a texture (or None for a plain colour) and a colour for the next shapes."""
    if texture_id is None:
        glDisable(GL_TEXTURE_2D)
    else:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(*color)


def box(width, height, depth):
    """A box centred at the origin. Each face shows the whole texture."""
    x, y, z = width / 2, height / 2, depth / 2
    faces = [
        # normal          four corners (counter-clockwise seen from outside)
        ((0, 0, 1), [(-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)]),        # front
        ((0, 0, -1), [(x, -y, -z), (-x, -y, -z), (-x, y, -z), (x, y, -z)]),   # back
        ((1, 0, 0), [(x, -y, z), (x, -y, -z), (x, y, -z), (x, y, z)]),        # right
        ((-1, 0, 0), [(-x, -y, -z), (-x, -y, z), (-x, y, z), (-x, y, -z)]),   # left
        ((0, 1, 0), [(-x, y, z), (x, y, z), (x, y, -z), (-x, y, -z)]),        # top
        ((0, -1, 0), [(-x, -y, -z), (x, -y, -z), (x, -y, z), (-x, -y, z)]),   # bottom
    ]
    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    glBegin(GL_QUADS)
    for normal, corners in faces:
        glNormal3f(*normal)
        for (u, v), corner in zip(tex_coords, corners):
            glTexCoord2f(u, v)
            glVertex3f(*corner)
    glEnd()


def sphere(radius):
    gluSphere(quadric(), radius, 24, 16)


def cylinder(radius, length):
    """A cylinder along the Z axis from z = 0 to z = length, closed at both ends."""
    gluCylinder(quadric(), radius, radius, length, 16, 1)
    glPushMatrix()
    glRotatef(180, 1, 0, 0)            # disks face +Z, so flip the first cap to face -Z
    gluDisk(quadric(), 0, radius, 16, 1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, length)         # second cap at the far end
    gluDisk(quadric(), 0, radius, 16, 1)
    glPopMatrix()

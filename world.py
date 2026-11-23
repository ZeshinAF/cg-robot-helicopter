"""The ground, the helipad and the round shadows under objects."""
from OpenGL.GL import (
    GL_BLEND, GL_LIGHTING, GL_QUADS, GL_TEXTURE_2D, glBegin, glColor4f, glDisable, glEnable,
    glEnd, glNormal3f, glPopMatrix, glPushMatrix, glRotatef, glTexCoord2f, glTranslatef, glVertex3f,
)
from OpenGL.GLU import gluDisk

import shapes
from textures import load_texture

HELIPAD = (8.0, 0.0)            # x, z of the helipad centre


class World:
    def __init__(self):
        self.grass = load_texture("textures/grass.png")
        self.helipad = load_texture("textures/helipad.png")

    def draw(self):
        # big grass square, the texture repeated 30 times in each direction
        shapes.use_texture(self.grass)
        self.flat_square(0, 0, 120, repeat=30, y=0.0)
        # helipad (6 x 6 m), slightly above the grass so they do not flicker
        shapes.use_texture(self.helipad)
        self.flat_square(HELIPAD[0], HELIPAD[1], 6, repeat=1, y=0.01)

    @staticmethod
    def flat_square(cx, cz, size, repeat, y):
        h = size / 2
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0); glVertex3f(cx - h, y, cz + h)
        glTexCoord2f(repeat, 0); glVertex3f(cx + h, y, cz + h)
        glTexCoord2f(repeat, repeat); glVertex3f(cx + h, y, cz - h)
        glTexCoord2f(0, repeat); glVertex3f(cx - h, y, cz - h)
        glEnd()


def draw_shadow(x, z, radius, darkness):
    """A soft dark circle on the ground under an object (a cheap 'blob' shadow)."""
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glColor4f(0, 0, 0, darkness)
    glPushMatrix()
    glTranslatef(x, 0.02, z)
    glRotatef(-90, 1, 0, 0)        # disks are drawn facing +Z; turn it to lie flat on the ground
    gluDisk(shapes.quadric(), 0, radius, 24, 1)
    glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

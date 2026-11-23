"""The helicopter: spinning rotors, take-off, flying, tilting and landing.

The helicopter faces +Z when its angle is 0. The rotors are animated by
adding (rotor speed x time) to their angle every frame.
"""
import math

import pygame
from OpenGL.GL import glPopMatrix, glPushMatrix, glRotatef, glScalef, glTranslatef

import shapes
from textures import load_texture


def approach(value, target, step):
    """Move value towards target by at most step (used for smooth changes)."""
    if value < target:
        return min(value + step, target)
    return max(value - step, target)


class Helicopter:
    MAX_ROTOR_SPEED = 1400.0   # degrees per second (about 4 turns per second)
    LIFT_ROTOR_SPEED = 1100.0  # rotor must spin at least this fast to take off
    CLIMB_SPEED = 3.0          # metres per second up / down
    MAX_SPEED = 8.0            # metres per second forward
    TURN_SPEED = 70.0          # degrees per second

    def __init__(self, x, z):
        self.x, self.y, self.z = x, 0.0, z
        self.angle = 0.0          # heading in degrees
        self.speed = 0.0          # forward speed
        self.rotor_angle = 0.0
        self.rotor_speed = 0.0
        self.pitch = 0.0          # nose down when flying forward
        self.roll = 0.0           # leans into turns
        self.camo = load_texture("textures/camo.png")
        self.metal = load_texture("textures/metal.png")

    @property
    def flying(self):
        return self.y > 0.05

    # ------------------------------------------------------------------ update
    def update(self, dt, keys):
        """keys = pygame key state when the player controls the helicopter, otherwise None."""
        forward = turn = climb = 0
        if keys is not None:
            forward = keys[pygame.K_w] - keys[pygame.K_s]
            turn = keys[pygame.K_a] - keys[pygame.K_d]
            climb = keys[pygame.K_q] - keys[pygame.K_e]

        # engine: runs while controlled or still in the air; rotors speed up / slow down gradually
        engine_on = keys is not None or self.flying
        target_rotor = self.MAX_ROTOR_SPEED if engine_on else 0.0
        self.rotor_speed = approach(self.rotor_speed, target_rotor, 500 * dt)
        self.rotor_angle = (self.rotor_angle + self.rotor_speed * dt) % 360

        # height: climb only when the rotor is fast enough; without a pilot it slowly lands
        if keys is None:
            climb = -0.6 if self.flying else 0
        if self.rotor_speed < self.LIFT_ROTOR_SPEED:
            climb = min(climb, 0)
        self.y = min(25.0, max(0.0, self.y + climb * self.CLIMB_SPEED * dt))

        # flying forward and turning only in the air
        if self.flying:
            self.speed = approach(self.speed, forward * self.MAX_SPEED, 6 * dt)
            self.angle += turn * self.TURN_SPEED * dt
        else:
            self.speed = 0.0
            turn = 0
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed * dt
        self.z += math.cos(rad) * self.speed * dt

        # tilt: nose down when moving forward, lean sideways when turning
        self.pitch = approach(self.pitch, 12 * self.speed / self.MAX_SPEED, 30 * dt)
        self.roll = approach(self.roll, -15 * turn, 40 * dt)

    # -------------------------------------------------------------------- draw
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 1, 0)      # heading
        glRotatef(self.pitch, 1, 0, 0)      # nose down
        glRotatef(self.roll, 0, 0, 1)       # lean into the turn

        # body: a stretched sphere with the camouflage texture
        shapes.use_texture(self.camo)
        glPushMatrix()
        glTranslatef(0, 1.2, 0)
        glScalef(1.0, 0.9, 1.8)
        shapes.sphere(0.8)
        glPopMatrix()

        # cockpit glass at the front
        shapes.use_texture(None, (0.35, 0.55, 0.75))
        glPushMatrix()
        glTranslatef(0, 1.35, 0.85)
        glScalef(0.75, 0.6, 0.7)
        shapes.sphere(0.8)
        glPopMatrix()

        # tail boom (a long cylinder going backwards) and the tail fin
        shapes.use_texture(self.camo)
        glPushMatrix()
        glTranslatef(0, 1.35, -1.0)
        glRotatef(180, 0, 1, 0)             # cylinders point along +Z; turn it to -Z
        shapes.cylinder(0.15, 3.2)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 1.75, -4.0)
        shapes.box(0.08, 0.8, 0.6)
        glPopMatrix()

        self.draw_tail_rotor()
        self.draw_main_rotor()
        self.draw_skids()
        glPopMatrix()

    def draw_main_rotor(self):
        shapes.use_texture(None, (0.2, 0.2, 0.22))
        glPushMatrix()
        glTranslatef(0, 1.85, 0)
        glRotatef(-90, 1, 0, 0)             # mast pointing up
        shapes.cylinder(0.07, 0.45)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 2.3, 0)
        glRotatef(self.rotor_angle, 0, 1, 0)   # <- the rotor animation
        shapes.sphere(0.14)                    # hub
        shapes.use_texture(self.metal, (0.5, 0.5, 0.55))
        for i in range(4):                     # four blades, 90 degrees apart
            glPushMatrix()
            glRotatef(90 * i, 0, 1, 0)
            glTranslatef(0, 0, 1.9)
            shapes.box(0.25, 0.04, 3.6)
            glPopMatrix()
        glPopMatrix()

    def draw_tail_rotor(self):
        glPushMatrix()
        glTranslatef(0.1, 1.85, -4.05)
        glRotatef(self.rotor_angle * 2, 1, 0, 0)   # spins twice as fast, around the X axis
        shapes.use_texture(self.metal, (0.5, 0.5, 0.55))
        shapes.box(0.03, 1.0, 0.12)
        shapes.box(0.03, 0.12, 1.0)
        glPopMatrix()

    def draw_skids(self):
        shapes.use_texture(None, (0.2, 0.2, 0.22))
        for side in (-1, 1):
            glPushMatrix()
            glTranslatef(0.75 * side, 0.08, -1.2)
            shapes.cylinder(0.06, 2.6)          # long tube along Z
            glPopMatrix()
            for z in (-0.6, 0.6):               # two struts up to the body
                glPushMatrix()
                glTranslatef(0.62 * side, 0.4, z)
                glRotatef(20 * side, 0, 0, 1)
                shapes.box(0.06, 0.65, 0.06)
                glPopMatrix()

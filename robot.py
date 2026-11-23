"""The robot: a body made of boxes that walks, looks around and waves.

The robot faces +Z when its angle is 0. All moving parts are animated with
sin(): the legs and arms swing in opposite directions while it walks.
"""
import math

import pygame
from OpenGL.GL import glColor3f, glPopMatrix, glPushMatrix, glRotatef, glTranslatef
from OpenGL.GLU import gluSphere

import shapes
from textures import load_texture


class Robot:
    WALK_SPEED = 2.0      # metres per second
    RUN_SPEED = 4.0
    TURN_SPEED = 120.0    # degrees per second

    def __init__(self, x, z):
        self.x, self.z = x, z
        self.angle = 0.0          # which way it faces (degrees around the Y axis)
        self.speed = 0.0          # current speed (negative = walking backwards)
        self.walk_phase = 0.0     # grows while walking; drives the leg/arm swing
        self.time = 0.0           # total time, used for idle animations
        self.wave_time = 0.0      # > 0 while the robot is waving
        self.metal = load_texture("textures/metal.png")
        self.face = load_texture("textures/robot_face.png")

    # ------------------------------------------------------------------ update
    def update(self, dt, keys):
        """keys = pygame key state when the player controls the robot, otherwise None."""
        self.time += dt
        target_speed = 0.0
        if keys is not None:
            fast = keys[pygame.K_LSHIFT]
            if keys[pygame.K_w]:
                target_speed = self.RUN_SPEED if fast else self.WALK_SPEED
            if keys[pygame.K_s]:
                target_speed = -self.WALK_SPEED / 2
            if keys[pygame.K_a]:
                self.angle += self.TURN_SPEED * dt
            if keys[pygame.K_d]:
                self.angle -= self.TURN_SPEED * dt

        # change speed gradually (accelerate / brake) instead of jumping
        self.speed += (target_speed - self.speed) * min(1.0, 8 * dt)

        # move in the direction the robot is facing
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed * dt
        self.z += math.cos(rad) * self.speed * dt

        # the faster it walks, the faster the legs swing
        self.walk_phase += self.speed * 3.0 * dt
        if self.wave_time > 0:
            self.wave_time -= dt

    def wave(self):
        self.wave_time = 2.5

    # -------------------------------------------------------------------- draw
    def draw(self):
        walking = min(1.0, abs(self.speed) / self.WALK_SPEED)   # 0 = standing, 1 = walking
        swing = 35 * math.sin(self.walk_phase) * walking        # leg / arm swing angle
        bob = 0.05 * abs(math.sin(self.walk_phase)) * walking   # body goes up and down
        breathe = 0.015 * math.sin(self.time * 2)               # small idle movement

        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glRotatef(self.angle, 0, 1, 0)

        # legs (hip joints 0.85 m above the ground)
        self.draw_leg(side=+1, swing=swing, knee=45 * max(0.0, -math.sin(self.walk_phase)) * walking)
        self.draw_leg(side=-1, swing=-swing, knee=45 * max(0.0, math.sin(self.walk_phase)) * walking)

        # everything above the hips moves up and down together
        glTranslatef(0, bob + breathe, 0)

        # body
        shapes.use_texture(self.metal)
        glPushMatrix()
        glTranslatef(0, 1.25, 0)
        shapes.box(0.7, 0.8, 0.4)
        glPopMatrix()

        self.draw_head()

        # arms swing opposite to the legs; the right arm waves when F is pressed
        self.draw_arm(side=+1, swing=-swing, raise_arm=0, wave=0)
        if self.wave_time > 0:
            self.draw_arm(side=-1, swing=0, raise_arm=150, wave=35 * math.sin(self.time * 10))
        else:
            self.draw_arm(side=-1, swing=swing, raise_arm=0, wave=0)

        glPopMatrix()

    def draw_head(self):
        look = 25 * math.sin(self.time * 0.7)        # slowly looks left and right
        glPushMatrix()
        glTranslatef(0, 1.65, 0)                     # neck, on top of the body
        glRotatef(look, 0, 1, 0)
        shapes.use_texture(None, (0.3, 0.3, 0.35))   # neck
        glPushMatrix()
        glTranslatef(0, 0.05, 0)
        shapes.box(0.15, 0.1, 0.15)
        glPopMatrix()

        glTranslatef(0, 0.3, 0)                      # head centre
        shapes.use_texture(self.metal)
        shapes.box(0.5, 0.42, 0.42)
        shapes.use_texture(self.face)                # face screen on the front
        glPushMatrix()
        glTranslatef(0, 0, 0.215)
        shapes.box(0.4, 0.32, 0.01)
        glPopMatrix()

        # antenna with a blinking light
        shapes.use_texture(None, (0.3, 0.3, 0.35))
        glPushMatrix()
        glTranslatef(0, 0.21, 0)
        glRotatef(-90, 1, 0, 0)                      # cylinders point along Z; turn it upwards
        shapes.cylinder(0.02, 0.25)
        glPopMatrix()
        blink = 0.5 + 0.5 * math.sin(self.time * 6)
        shapes.use_texture(None)
        glColor3f(1.0, 0.2 + 0.6 * blink, 0.1)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        gluSphere(shapes.quadric(), 0.05, 12, 8)
        glPopMatrix()
        glPopMatrix()

    def draw_arm(self, side, swing, raise_arm, wave):
        """side = +1 left, -1 right. Rotations happen at the shoulder, then the elbow."""
        glPushMatrix()
        glTranslatef(0.45 * side, 1.55, 0)           # shoulder joint
        glRotatef(-swing, 1, 0, 0)                   # swing forward / back
        glRotatef(raise_arm * side, 0, 0, 1)         # lift sideways (for waving)
        shapes.use_texture(None, (0.3, 0.3, 0.35))
        shapes.sphere(0.12)                          # shoulder ball
        shapes.use_texture(self.metal)
        glTranslatef(0, -0.22, 0)
        shapes.box(0.16, 0.4, 0.16)                  # upper arm
        glTranslatef(0, -0.22, 0)                    # elbow joint
        glRotatef(wave * side, 0, 0, 1)              # forearm waves
        glRotatef(-15, 1, 0, 0)                      # elbow slightly bent
        glTranslatef(0, -0.2, 0)
        shapes.box(0.14, 0.38, 0.14)                 # forearm
        glTranslatef(0, -0.24, 0)
        shapes.use_texture(None, (0.3, 0.3, 0.35))
        shapes.sphere(0.09)                          # hand
        glPopMatrix()

    def draw_leg(self, side, swing, knee):
        glPushMatrix()
        glTranslatef(0.2 * side, 0.85, 0)            # hip joint
        glRotatef(-swing, 1, 0, 0)                   # swing forward / back
        shapes.use_texture(self.metal)
        glTranslatef(0, -0.2, 0)
        shapes.box(0.2, 0.42, 0.2)                   # thigh
        glTranslatef(0, -0.21, 0)                    # knee joint
        glRotatef(knee, 1, 0, 0)                     # knee bends backwards
        shapes.use_texture(None, (0.3, 0.3, 0.35))
        shapes.sphere(0.1)
        shapes.use_texture(self.metal)
        glTranslatef(0, -0.2, 0)
        shapes.box(0.18, 0.4, 0.18)                  # shin
        glTranslatef(0, -0.2, 0.06)
        shapes.use_texture(None, (0.25, 0.25, 0.3))
        shapes.box(0.24, 0.06, 0.36)                 # foot
        glPopMatrix()

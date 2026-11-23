"""Robot & Helicopter - Computer Graphics course project.

Run:  python main.py
Tab switches between the robot and the helicopter.
"""
import math

import pygame
from OpenGL.GL import (
    GL_AMBIENT, GL_COLOR_BUFFER_BIT, GL_COLOR_MATERIAL, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_DIFFUSE, GL_LIGHT0, GL_LIGHTING, GL_MODELVIEW, GL_NORMALIZE, GL_ONE_MINUS_SRC_ALPHA,
    GL_POSITION, GL_PROJECTION, GL_SRC_ALPHA, glBlendFunc, glClear, glClearColor, glEnable,
    glLightfv, glLoadIdentity, glMatrixMode, glViewport,
)
from OpenGL.GLU import gluLookAt, gluPerspective

from helicopter import Helicopter
from robot import Robot
from world import HELIPAD, World, draw_shadow

WIDTH, HEIGHT = 1280, 720


class Camera:
    """Orbits around a target point. Drag with the left mouse button, zoom with the wheel."""

    def __init__(self):
        self.yaw = 35.0        # degrees around the target (start in front of the robot)
        self.pitch = 20.0      # degrees above the ground
        self.distance = 8.0
        self.target = [0.0, 1.0, 0.0]

    def follow(self, x, y, z, dt):
        # move a part of the way to the new target every frame -> smooth camera motion
        k = min(1.0, 5 * dt)
        for i, value in enumerate((x, y, z)):
            self.target[i] += (value - self.target[i]) * k

    def apply(self):
        yaw, pitch = math.radians(self.yaw), math.radians(self.pitch)
        tx, ty, tz = self.target
        eye_x = tx + self.distance * math.cos(pitch) * math.sin(yaw)
        eye_y = ty + self.distance * math.sin(pitch)
        eye_z = tz + self.distance * math.cos(pitch) * math.cos(yaw)
        gluLookAt(eye_x, eye_y, eye_z, tx, ty, tz, 0, 1, 0)


def init_opengl():
    glClearColor(0.55, 0.75, 0.95, 1)                # sky blue background
    glEnable(GL_DEPTH_TEST)                          # near objects hide far ones
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)                              # one light = the sun
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 0.95, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.45, 1))
    glEnable(GL_COLOR_MATERIAL)                      # glColor sets the surface colour
    glEnable(GL_NORMALIZE)                           # keep lighting right on scaled shapes
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # for the transparent shadows


def keep_apart(robot, heli):
    """Simple collision: the robot cannot walk into the landed helicopter."""
    if heli.y > 2.5:                                 # helicopter is high in the air
        return
    dx, dz = robot.x - heli.x, robot.z - heli.z
    distance = math.hypot(dx, dz)
    min_distance = 2.3
    if 0 < distance < min_distance:
        robot.x = heli.x + dx / distance * min_distance
        robot.z = heli.z + dz / distance * min_distance


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    init_opengl()

    world = World()
    robot = Robot(0, 0)
    heli = Helicopter(*HELIPAD)
    camera = Camera()
    active = robot                                   # who the keys control
    clock = pygame.time.Clock()
    dragging = False

    running = True
    while running:
        dt = min(clock.tick(60) / 1000.0, 0.05)      # seconds since the last frame

        # ---- input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    active = heli if active is robot else robot
                elif event.key == pygame.K_f and active is robot:
                    robot.wave()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                camera.yaw -= event.rel[0] * 0.3
                camera.pitch = max(-5, min(80, camera.pitch + event.rel[1] * 0.3))
            elif event.type == pygame.MOUSEWHEEL:
                camera.distance = max(3, min(40, camera.distance - event.y))
        keys = pygame.key.get_pressed()

        # ---- update (only the active object gets the keys)
        robot.update(dt, keys if active is robot else None)
        heli.update(dt, keys if active is heli else None)
        keep_apart(robot, heli)
        if active is robot:
            camera.follow(robot.x, 1.2, robot.z, dt)
        else:
            camera.follow(heli.x, heli.y + 1.5, heli.z, dt)

        # ---- draw
        glViewport(0, 0, WIDTH, HEIGHT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, WIDTH / HEIGHT, 0.1, 300)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        camera.apply()
        glLightfv(GL_LIGHT0, GL_POSITION, (0.4, 1.0, 0.3, 0))   # sun direction (0 = far away)

        world.draw()
        draw_shadow(robot.x, robot.z, 0.6, 0.35)
        draw_shadow(heli.x, heli.z, 2.2, 0.35 * max(0.0, 1 - heli.y / 25))
        robot.draw()
        heli.draw()

        if active is robot:
            title = "ROBOT  |  W/S walk, A/D turn, Shift run, F wave  |  Tab: helicopter  |  mouse drag: camera, wheel: zoom"
        else:
            title = (f"HELICOPTER  |  height {heli.y:4.1f} m  |  Q/E up/down, W/S forward/back, A/D turn"
                     "  |  Tab: robot  |  mouse drag: camera, wheel: zoom")
        pygame.display.set_caption(title)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

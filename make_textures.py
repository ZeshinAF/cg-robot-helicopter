"""Creates the PNG images in the textures/ folder (run once: python make_textures.py).

You do not need this file to run the project - the images are already there.
You can also replace any PNG with a photo from the internet (keep the file name).
"""
import os
import random

import pygame

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "textures")


def speckle(surface, colors, count, size):
    """Sprinkle random small rectangles - a cheap 'natural' look."""
    w, h = surface.get_size()
    for _ in range(count):
        c = random.choice(colors)
        surface.fill(c, (random.randrange(w), random.randrange(h), size, size))


def grass():
    s = pygame.Surface((256, 256))
    s.fill((70, 135, 55))
    speckle(s, [(60, 120, 45), (85, 150, 60), (55, 110, 40), (95, 160, 70)], 6000, 3)
    return s


def metal():
    s = pygame.Surface((256, 256))
    s.fill((165, 170, 180))
    for y in range(0, 256, 2):                                   # brushed metal lines
        shade = random.randint(150, 185)
        pygame.draw.line(s, (shade, shade + 4, shade + 10), (0, y), (255, y))
    for x, y in ((12, 12), (244, 12), (12, 244), (244, 244)):    # rivets in the corners
        pygame.draw.circle(s, (110, 115, 125), (x, y), 6)
        pygame.draw.circle(s, (200, 205, 215), (x - 2, y - 2), 2)
    pygame.draw.rect(s, (120, 125, 135), (0, 0, 256, 256), 4)    # panel edge
    return s


def robot_face():
    s = pygame.Surface((256, 256))
    s.fill((25, 30, 40))                                         # dark screen
    pygame.draw.rect(s, (90, 95, 105), (0, 0, 256, 256), 14)     # frame
    for x in (80, 176):                                          # glowing eyes
        pygame.draw.circle(s, (40, 200, 255), (x, 105), 28)
        pygame.draw.circle(s, (200, 245, 255), (x, 105), 12)
    pygame.draw.arc(s, (40, 200, 255), (70, 120, 116, 80), 3.6, 5.8, 8)   # smile
    return s


def camo():
    s = pygame.Surface((256, 256))
    s.fill((85, 95, 55))
    for color in ((60, 70, 40), (120, 115, 75), (45, 50, 35)):   # random blobs
        for _ in range(40):
            x, y = random.randrange(256), random.randrange(256)
            pygame.draw.ellipse(s, color, (x, y, random.randint(20, 60), random.randint(15, 40)))
    return s


def helipad():
    s = pygame.Surface((256, 256))
    s.fill((70, 72, 75))                                         # concrete
    speckle(s, [(60, 62, 65), (85, 87, 90)], 3000, 2)
    pygame.draw.circle(s, (240, 200, 40), (128, 128), 110, 10)   # yellow circle
    pygame.draw.rect(s, (240, 240, 240), (78, 68, 22, 120))      # the letter H
    pygame.draw.rect(s, (240, 240, 240), (156, 68, 22, 120))
    pygame.draw.rect(s, (240, 240, 240), (100, 117, 56, 22))
    return s


def main():
    random.seed(1)
    os.makedirs(OUT, exist_ok=True)
    for name, make in (("grass", grass), ("metal", metal), ("robot_face", robot_face),
                       ("camo", camo), ("helipad", helipad)):
        pygame.image.save(make(), os.path.join(OUT, name + ".png"))
        print("saved", name + ".png")


if __name__ == "__main__":
    main()

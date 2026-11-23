"""Loading image files (PNG/JPG) into OpenGL textures."""
import pygame
from OpenGL.GL import (
    GL_LINEAR, GL_LINEAR_MIPMAP_LINEAR, GL_REPEAT, GL_RGBA, GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_UNSIGNED_BYTE, glBindTexture, glGenTextures, glTexParameteri,
)
from OpenGL.GLU import gluBuild2DMipmaps


def load_texture(path):
    """Read an image file and upload it to the graphics card. Returns the texture id."""
    image = pygame.image.load(path)
    width, height = image.get_size()
    pixels = pygame.image.tostring(image, "RGBA", True)  # True = flip (OpenGL starts at the bottom)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
    return texture_id

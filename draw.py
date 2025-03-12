import pygame, sys
import pygame.draw as draw
import pygame.gfxdraw
import time
import math


def aacircle(surface, x, y, r, color):
    pygame.gfxdraw.filled_circle(surface, x, y, r, color)
    pygame.gfxdraw.aacircle(surface, x, y, r, color)

def aacircle_outline(surface, x, y, r, color, width):
    pygame.draw.circle(surface, color, (x,y), r, width)
    pygame.gfxdraw.aacircle(surface, x,y, r, color)
    pygame.gfxdraw.aacircle(surface, x-1,y-1, r, color)
    pygame.gfxdraw.aacircle(surface, x-1,y, r, color)
    pygame.gfxdraw.aacircle(surface, x,y-1, r, color)

    pygame.gfxdraw.aacircle(surface, x,y, r-width, color)
    pygame.gfxdraw.aacircle(surface, x-1,y-1, r-width, color)
    pygame.gfxdraw.aacircle(surface, x-1,y, r-width, color)
    pygame.gfxdraw.aacircle(surface, x,y-1, r-width, color)

def aaline(surface, color, start, end, width):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = int(max(abs(dx), abs(dy)))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        aacircle(surface, x, y, width, color)

def aatriangle(surface, color, x, y, size, angle):
    draw.polygon(surface, color, ((x,y),(x+size*math.cos(angle),y+size*math.sin(angle)),(x+size*math.cos(angle+math.pi/2),y+size*math.sin(angle+math.pi/2))))

def text(screen, font, msg, color, pos):
    text_render = font.render(msg, 1, color)
    screen.blit(text_render, pos)
    return text_render
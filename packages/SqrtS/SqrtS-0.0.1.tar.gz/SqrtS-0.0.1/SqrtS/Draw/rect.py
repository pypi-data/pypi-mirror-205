import pygame


def draw_rect(screen, color, rect, border_width):
    pygame.draw.rect(screen, color, rect, border_width)


def draw_polygon(screen, color, pointlist, border_width):
   pygame.draw.polygon(screen, color, pointlist, width=border_width)



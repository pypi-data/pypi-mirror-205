import pygame


def draw_circle(screen, color, pos, radius, border_width):
    pygame.draw.circle(screen, color, pos, radius, border_width)


def draw_ellipse(screen, color, rect, border_width):
    pygame.draw.ellipse(screen, color, rect, border_width)


def draw_arc(screen, color, rect, start_angle, stop_angle, border_width):
    pygame.draw.arc(screen, color, rect, start_angle, stop_angle, border_width)



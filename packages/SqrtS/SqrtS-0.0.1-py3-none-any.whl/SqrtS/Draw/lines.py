import pygame


class Line:
    def __init__(self, color, start_pos, end_pos, border_width):
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.border_width = border_width

    def blit(self, screen):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.border_width)


class Lines:
    def __init__(self, color, if_closed, border_width, points):
        self.color = color
        self.if_closed = if_closed
        self.border_width = border_width
        self.points = points

    def blit(self, screen):
        pygame.draw.lines(screen, self.color, self.if_closed, self.points, self.border_width)


class AALine:
    def __init__(self, color, if_closed, border_width, points):
        self.color = color
        self.if_closed = if_closed
        self.border_width = border_width
        self.points = points

    def blit(self, screen):
        pygame.draw.aaline(screen, self.color, self.if_closed, self.points, self.border_width)


class AALines:
    def __init__(self, color, if_closed, border_width, points):
        self.color = color
        self.if_closed = if_closed
        self.border_width = border_width
        self.points = points

    def blit(self, screen):
        pygame.draw.aalines(screen, self.color, self.if_closed, self.points, self.border_width)

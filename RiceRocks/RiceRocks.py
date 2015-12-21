import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 640))
while 1:
    screen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
import pygame
from pygame.locals import *

from game_world import World

pygame.init()

screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hardest Game")

tile_size = 200
clock = pygame.time.Clock()
fps = 60

level1_data = [
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
]

level1 = World(level1_data, tile_size)

deaths = 0

run = True
while run:
    clock.tick(fps)
    screen.fill((255, 255, 255))
    level1.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

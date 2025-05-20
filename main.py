import pygame
from pygame.locals import *

from game_world import World
from player import Player
from player import Obstacle

pygame.init()

screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hardest Game")

tile_size = 50
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
player = Player(0, 0, tile_size)
obstacle = Obstacle(100, 50, tile_size)

run = True
while run:
    clock.tick(fps)
    screen.fill((255, 255, 255))
    level1.draw()

    player.update()
    obstacle.update()
    if player.rect.colliderect(obstacle):
        deaths += 1
        print(f"Deaths: {deaths}")
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

import pygame
from pygame.locals import *

from game_world import World
from player import Obstacle, Player

pygame.init()

black = (0, 0, 0)

screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hardest Game")

tile_size = 50
clock = pygame.time.Clock()
fps = 60

level1_data = [
    [0, 0, 0, 2, 2, 1, 0, 1, 0],
    [1, 0, 1, 2, 2, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
]

level1 = World(level1_data, tile_size)

deaths = 0
player = Player(0, 0, tile_size)
obstacle = Obstacle(100, 25, tile_size)

font = pygame.font.Font("freesansbold.ttf", 32)


run = True
while run:
    clock.tick(fps)
    screen.fill((255, 255, 255))
    level1.draw()

    player.update(level1)
    obstacle.update()

    # Display and update death message
    death_message = f"Deaths: {deaths}"
    text = font.render(death_message, True, black)
    textbox = text.get_rect()

    if player.rect.colliderect(obstacle):
        player.respawn()
        deaths += 1
        print(death_message)

    screen.blit(text, textbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

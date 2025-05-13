import pygame

from game_world import World

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))


class Player:
    def __init__(self, x, y, tile_size):
        img = pygame.image.load("img/player.jpg")
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player_size = tile_size * 5 / 8

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 1

        screen.blit(self.image, self.rect)

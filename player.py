import pygame

from game_world import World

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))


class Player:
    def __init__(self, x, y, size):
        img = pygame.image.load("player.png")
        self.image = pygame.transform.scale(img, (size * 5 / 8, size * 5 / 8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= 1

        if key[pygame.K_d]:
            self.rect.x += 1

        if key[pygame.K_w]:
            self.rect.y -= 1

        if key[pygame.K_s]:
            self.rect.y += 1

        screen.blit(self.image, self.rect)


class Obstacle(Player):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        img = pygame.image.load("obstacle.png")
        self.image = pygame.transform.scale(img, (size * 5 / 8, size * 5 / 8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        screen.blit(self.image, self.rect)

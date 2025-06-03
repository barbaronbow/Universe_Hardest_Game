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

        self.spawnpoint = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, level_data: World):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx -= 1

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx += 1

        if key[pygame.K_w] or key[pygame.K_UP]:
            dy -= 1

        if key[pygame.K_s] or key[pygame.K_DOWN]:
            dy += 1

        for tile in level_data.tile_list:
            # check for collision in x direction
            if tile[2]:
                if tile[1].colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
                    dy = 0

            else:
                if tile[1].colliderect(
                    self.rect.x, self.rect.y, self.width, self.height
                ):
                    self.spawnpoint = (
                        self.rect.x + self.width,
                        self.rect.y + self.height,
                    )

        self.rect.x += dx
        self.rect.y += dy
        screen.blit(self.image, self.rect)

    def respawn(self):
        self.rect.x = self.spawnpoint[0]
        self.rect.y = self.spawnpoint[1]


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

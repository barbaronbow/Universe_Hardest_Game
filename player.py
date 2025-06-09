# player.py - Enhanced version
import pygame

from game_world import World

white = (255, 255, 255)
yellow = (255, 255, 0)

screen_width = 1800  # Updated to match main.py
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))


class Player:
    def __init__(self, x, y, size):
        try:
            img = pygame.image.load("player.png")
        except pygame.error:
            # Create a simple colored rectangle if image not found
            img = pygame.Surface((size * 5 // 8, size * 5 // 8))
            img.fill((0, 0, 255))  # Blue player
            
        self.image = pygame.transform.scale(img, (size * 5 // 8, size * 5 // 8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.spawnpoint = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 3  # Added speed control

    def update(self, level_data: World):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx -= self.speed

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx += self.speed

        if key[pygame.K_w] or key[pygame.K_UP]:
            dy -= self.speed

        if key[pygame.K_s] or key[pygame.K_DOWN]:
            dy += self.speed

        # Collision detection
        for tile in level_data.tile_list:
            # Check for collision in x direction
            if tile[2]:  # If tile is collidable
                if tile[1].colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    dx = 0
                # Check for collision in y direction
                if tile[1].colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
                    dy = 0

            # Handle safe zones (checkpoints)
            elif not tile[2] and tile[3] == 'checkpoint':  # Safe zone
                if tile[1].colliderect(
                    self.rect.x, self.rect.y, self.width, self.height
                ):
                    # Update spawnpoint when touching safe zone
                    self.spawnpoint = (self.rect.x, self.rect.y)

        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Keep player within screen bounds
        self.rect.x = max(0, min(self.rect.x, screen_width - self.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.height))
        
        # Draw player
        screen.blit(self.image, self.rect)

    def respawn(self):
        self.rect.x = self.spawnpoint[0]
        self.rect.y = self.spawnpoint[1]


class Obstacle:
    def __init__(self, x, y, size):
        try:
            img = pygame.image.load("obstacle.png")
        except pygame.error:
            # Create a simple red circle if image not found
            img = pygame.Surface((size * 5 // 8, size * 5 // 8))
            img.fill(white)
            img.set_colorkey(white)
            pygame.draw.circle(img, (255, 0, 0), 
                             (size * 5 // 16, size * 5 // 16), size * 5 // 16)
        
        self.image = img.convert()
        self.image.set_colorkey(white)
        self.image = pygame.transform.scale(self.image, (size * 5 // 8, size * 5 // 8))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)


class Coin:
    def __init__(self, x, y, size):
        try:
            img = pygame.image.load("coin.png")
        except pygame.error:
            # Create a simple yellow circle if image not found
            img = pygame.Surface((size // 2, size // 2))
            img.fill(white)
            img.set_colorkey(white)
            pygame.draw.circle(img, yellow, (size // 4, size // 4), size // 4)
            # Add a simple border
            pygame.draw.circle(img, (255, 215, 0), (size // 4, size // 4), size // 4, 2)
            
        self.image = img.convert()
        self.image.set_colorkey(white)
        self.image = pygame.transform.scale(self.image, (size // 2, size // 2))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation properties
        self.original_y = y
        self.bounce_height = 5
        self.bounce_speed = 0.1
        self.time = 0

    def update(self):
        # Add a gentle bouncing animation
        self.time += self.bounce_speed
        bounce_offset = int(self.bounce_height * abs(pygame.math.Vector2(0, 1).rotate(self.time * 180).y))
        self.rect.y = self.original_y - bounce_offset
        
        screen.blit(self.image, self.rect)

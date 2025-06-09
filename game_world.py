# game_world.py - Enhanced version
import pygame

screen_width = 1800  # Updated to match main.py
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))

# Colors for tiles
wall_color = (100, 100, 100)
checkpoint_color = (0, 255, 0, 128)  # Semi-transparent green
goal_color = (0, 200, 0)  # Darker green for goal


class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.tile_size = tile_size

        # Try to load images, create colored rectangles as fallback
        try:
            wall_img = pygame.image.load("wall.jpg")
        except pygame.error:
            wall_img = pygame.Surface((tile_size, tile_size))
            wall_img.fill(wall_color)
            
        try:
            checkpoint_img = pygame.image.load("checkpoint.jpg")
        except pygame.error:
            checkpoint_img = pygame.Surface((tile_size, tile_size))
            checkpoint_img.fill(checkpoint_color[:3])
            checkpoint_img.set_alpha(128)  # Make semi-transparent

        # Create goal zone image
        goal_img = pygame.Surface((tile_size, tile_size))
        goal_img.fill(goal_color)

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Wall
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    collidable = True
                    tile_data = (img, img_rect, collidable, 'wall')
                    self.tile_list.append(tile_data)
                    
                elif tile == 2:  # Checkpoint/Safe zone
                    img = pygame.transform.scale(checkpoint_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    collidable = False
                    tile_data = (img, img_rect, collidable, 'checkpoint')
                    self.tile_list.append(tile_data)
                    
                elif tile == 3:  # Goal zone
                    img = pygame.transform.scale(goal_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    collidable = False
                    tile_data = (img, img_rect, collidable, 'goal')
                    self.tile_list.append(tile_data)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

import pygame

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))


class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.tile_size = tile_size

        wall_img = pygame.image.load("wall.jpg")
        checkpoint_img = pygame.image.load("checkpoint.jpg")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: # Wall
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    collidable = True
                    tile = (img, img_rect, collidable)
                    self.tile_list.append(tile)
                if tile == 2: # Checkpoint
                    img = pygame.transform.scale(checkpoint_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    collidable = False
                    tile = (img, img_rect, collidable)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

import pygame

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))


class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.tile_size = tile_size

        wall_img = pygame.image.load("img/wall.jpg")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

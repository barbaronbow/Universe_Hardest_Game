import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game window
tile_size = 50
cols = 36
rows = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * rows) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# Load images
checkpoint = pygame.image.load("checkpoint.jpg")
wall = pygame.image.load("wall.jpg")
save_img = pygame.image.load("save_image.png")
load_img = pygame.image.load("load_button.png")

# Define game variables
clicked = False
level = 1

# Define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

# Create empty tile list with dimensions 20x36 (rows x cols)
world_data = [[0 for _ in range(cols)] for _ in range(rows)]

# Create boundary walls
for row in range(rows):
    for col in range(cols):
        if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
            world_data[row][col] = 1

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_grid():
    for c in range(cols + 1):
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
    for r in range(rows + 1):
        pygame.draw.line(screen, white, (0, r * tile_size), (screen_width, r * tile_size))

def draw_world():
    for row in range(rows):
        for col in range(cols):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                elif world_data[row][col] == 2:
                    img = pygame.transform.scale(checkpoint, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Create buttons
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

# Main game loop
run = True
while run:
    clock.tick(fps)
    screen.fill(green)

    if save_button.draw():
        with open(f'level{level}_data', 'wb') as f:
            pickle.dump(world_data, f)

    if load_button.draw():
        if path.exists(f'level{level}_data'):
            with open(f'level{level}_data', 'rb') as f:
                world_data = pickle.load(f)

    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            if x < cols and y < rows:
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 8:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 8
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    pygame.display.update()

pygame.quit()


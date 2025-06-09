import csv
import os
import pickle

import pygame


# Create a simple button class since we don't have the external button module
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode(
    (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN)
)
pygame.display.set_caption("Level Editor")

# define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = 100
TILE_TYPES = 21  # Increased to accommodate more tile types
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


# Function to create a placeholder tile image
def create_placeholder_tile(tile_id, size):
    surface = pygame.Surface((size, size))

    # Different colors for different tile types
    colors = [
        (139, 69, 19),  # Brown (dirt/ground)
        (128, 128, 128),  # Gray (stone)
        (34, 139, 34),  # Green (grass)
        (65, 105, 225),  # Blue (water)
        (255, 255, 0),  # Yellow (sand)
        (255, 165, 0),  # Orange (lava)
        (160, 82, 45),  # Saddle brown (wood)
        (0, 100, 0),  # Dark green (tree)
        (255, 192, 203),  # Pink (special)
        (128, 0, 128),  # Purple (magic)
        (255, 20, 147),  # Deep pink (gem)
        (0, 255, 255),  # Cyan (ice)
        (255, 69, 0),  # Red orange (fire)
        (50, 205, 50),  # Lime green (slime)
        (70, 130, 180),  # Steel blue (metal)
        (218, 165, 32),  # Golden rod (gold)
        (186, 85, 211),  # Medium orchid (crystal)
        (255, 228, 181),  # Moccasin (brick)
        (47, 79, 79),  # Dark slate gray (rock)
        (250, 128, 114),  # Salmon (coral)
        (255, 255, 255),  # White (cloud)
    ]

    color = colors[tile_id % len(colors)]
    surface.fill(color)

    # Add a border
    pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)

    # Add tile number
    font = pygame.font.Font(None, 24)
    text = font.render(
        str(tile_id), True, (255, 255, 255) if sum(color) < 400 else (0, 0, 0)
    )
    text_rect = text.get_rect(center=(size // 2, size // 2))
    surface.blit(text, text_rect)

    return surface


# Load or create tile images
img_list = []
for x in range(TILE_TYPES):
    img_path = f"{x}.jpg"
    if os.path.exists(img_path):
        try:
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)
        except pygame.error:
            # If image fails to load, create placeholder
            img_list.append(create_placeholder_tile(x, TILE_SIZE))
    else:
        # Create placeholder tile if image doesn't exist
        img_list.append(create_placeholder_tile(x, TILE_SIZE))


# Create placeholder images for save/load buttons if they don't exist
def create_button_image(text, width=100, height=40):
    surface = pygame.Surface((width, height))
    surface.fill((100, 100, 100))
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)

    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface, text_rect)

    return surface


# Load or create button images
if os.path.exists("save_image.png"):
    save_img = pygame.image.load("save_image.png").convert_alpha()
else:
    save_img = create_button_image("SAVE")

if os.path.exists("load_button.png"):
    load_img = pygame.image.load("load_button.png").convert_alpha()
else:
    load_img = create_button_image("LOAD")

# define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont("Futura", 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# draw grid
def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(
            screen,
            WHITE,
            (c * TILE_SIZE - scroll, 0),
            (c * TILE_SIZE - scroll, SCREEN_HEIGHT),
        )
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(
            screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE)
        )


# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0 and tile < len(img_list):
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# create buttons
save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button(
    SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1
)

# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(
        SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1
    )
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:
    clock.tick(FPS)

    # Fill background
    screen.fill(BLACK)

    draw_grid()
    draw_world()

    draw_text(f"Level: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text(
        "Press UP or DOWN to change level",
        font,
        WHITE,
        10,
        SCREEN_HEIGHT + LOWER_MARGIN - 60,
    )

    # save and load data
    if save_button.draw(screen):
        # save level data
        try:
            with open(f"level{level}_data.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                for row in world_data:
                    writer.writerow(row)
            print(f"Level {level} saved successfully!")
        except Exception as e:
            print(f"Error saving level: {e}")

    if load_button.draw(screen):
        # load in level data
        scroll = 0
        try:
            with open(f"level{level}_data.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        if x < ROWS and y < MAX_COLS:
                            world_data[x][y] = int(tile)
            print(f"Level {level} loaded successfully!")
        except FileNotFoundError:
            print(f"Level {level} file not found!")
        except Exception as e:
            print(f"Error loading level: {e}")

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    if current_tile < len(button_list):
        pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # Display current tile info
    draw_text(
        f"Current Tile: {current_tile}",
        font,
        WHITE,
        SCREEN_WIDTH + 10,
        SCREEN_HEIGHT - 40,
    )

    # scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if 0 <= y < ROWS and 0 <= x < MAX_COLS:
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            if 0 <= y < ROWS and 0 <= x < MAX_COLS:
                world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()

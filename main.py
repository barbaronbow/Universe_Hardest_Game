# main.py - Enhanced version with 5 BRUTAL levels
import math

import pygame
from pygame.locals import *

from game_world import World
from player import Coin, Obstacle, Player

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The World's Hardest Game - 5 Levels")

tile_size = 100
clock = pygame.time.Clock()
fps = 60

# Level designs - 0: empty, 1: wall, 2: safe zone/checkpoint, 3: goal zone
level_data = [
    # Level 1 - "The Gauntlet" - Simple but deadly corridor
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 1],
        [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
]

level_coins = [
    # Level 1: 3 coins in the path of moving obstacles
    [(300, 450), (800, 250), (1200, 650)],
    [(550, 600), (800, 250), (1150, 600)],
]

# Moving obstacle patterns for each level - BRUTAL difficulty
level_obstacles = [
    # Level 1: 4 horizontal sweepers at different speeds and heights
    [
        {"x": 850, "y": 200, "pattern": "horizontal", "range": 1550, "speed": 0.2},
        {"x": 850, "y": 300, "pattern": "horizontal", "range": 1550, "speed": -0.2},
        {"x": 850, "y": 400, "pattern": "horizontal", "range": 1550, "speed": 0.4},
        {"x": 850, "y": 500, "pattern": "horizontal", "range": 1550, "speed": -0.2},
        {"x": 850, "y": 600, "pattern": "horizontal", "range": 1550, "speed": 0.2},
        {"x": 850, "y": 700, "pattern": "horizontal", "range": 1550, "speed": -0.2},
        {"x": 850, "y": 800, "pattern": "horizontal", "range": 1550, "speed": 0.2},
    ],
    [
        {"x": 550, "y": 600, "pattern": "circle", "range": 250, "speed": 0.3},
        {"x": 550, "y": 600, "pattern": "circle", "range": 150, "speed": 0.3},
        {"x": 550, "y": 600, "pattern": "circle", "range": 125, "speed": 0.3},
        {"x": 550, "y": 600, "pattern": "circle", "range": 250, "speed": -0.3},
        {"x": 550, "y": 600, "pattern": "circle", "range": 150, "speed": -0.3},
        {"x": 550, "y": 600, "pattern": "circle", "range": 125, "speed": -0.3},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 250, "speed": 0.3},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 250, "speed": -0.3},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 150, "speed": -0.3},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 150, "speed": 0.3},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 125, "speed": 0.4},
        {"x": 1150, "y": 600, "pattern": "circle", "range": 125, "speed": -0.3},
    ],
]


class MovingObstacle(Obstacle):
    def __init__(self, x, y, size, pattern="horizontal", movement_range=100, speed=2):
        super().__init__(x, y, size)
        self.start_x = x
        self.start_y = y
        self.pattern = pattern
        self.range = movement_range
        self.speed = speed
        self.time = 0
        self.direction = 1

    def update(self):
        self.time += 0.1

        if self.pattern == "horizontal":
            # Move back and forth horizontally
            offset = math.sin(self.time * self.speed) * self.range / 2
            self.rect.x = self.start_x + offset

        elif self.pattern == "vertical":
            # Move back and forth vertically
            offset = math.sin(self.time * self.speed) * self.range / 2
            self.rect.y = self.start_y + offset

        elif self.pattern == "circle":
            # Move in a circular pattern
            self.rect.x = self.start_x + math.cos(self.time * self.speed) * self.range
            self.rect.y = self.start_y + math.sin(self.time * self.speed) * self.range

        # Draw the obstacle
        screen.blit(self.image, self.rect)


class GameManager:
    def __init__(self):
        self.current_level = 0
        self.deaths = 0
        self.total_deaths = 0
        self.levels = []
        self.coins = []
        self.obstacles = []
        self.coins_collected = 0
        self.coins_needed = 0
        self.player = Player(75, 75, tile_size)
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.load_level(0)

    def load_level(self, level_num):
        if level_num >= len(level_data):
            return False

        self.current_level = level_num
        self.deaths = 0

        # Load world
        self.world = World(level_data[level_num], tile_size)

        # Reset player position
        self.player.rect.x = 100
        self.player.rect.y = 100
        self.player.spawnpoint = (100, 100)

        # Load coins
        self.coins = []
        for coin_pos in level_coins[level_num]:
            self.coins.append(Coin(coin_pos[0], coin_pos[1], tile_size))

        self.coins_collected = 0
        self.coins_needed = len(self.coins)

        # Load moving obstacles
        self.obstacles = []
        for obs_data in level_obstacles[level_num]:
            obstacle = MovingObstacle(
                obs_data["x"],
                obs_data["y"],
                tile_size,
                obs_data["pattern"],
                obs_data["range"],
                obs_data["speed"],
            )
            self.obstacles.append(obstacle)

        return True

    def check_goal(self):
        # Check if player reached goal zone (tile type 3)
        player_tile_x = self.player.rect.x // tile_size
        player_tile_y = self.player.rect.y // tile_size

        if player_tile_y < len(level_data[self.current_level]) and player_tile_x < len(
            level_data[self.current_level][0]
        ):

            tile_type = level_data[self.current_level][player_tile_y][player_tile_x]
            if tile_type == 3 and self.coins_collected >= self.coins_needed:
                return True
        return False

    def update(self):
        # Update world and player
        self.world.draw()
        self.player.update(self.world)

        # Update and check coin collection
        coins_to_remove = []
        for i, coin in enumerate(self.coins):
            coin.update()
            if self.player.rect.colliderect(coin.rect):
                coins_to_remove.append(i)
                self.coins_collected += 1

        # Remove collected coins
        for i in reversed(coins_to_remove):
            del self.coins[i]

        # Update moving obstacles
        player_hit = False
        for obstacle in self.obstacles:
            obstacle.update()
            if self.player.rect.colliderect(obstacle.rect):
                player_hit = True

        # Handle player death
        if player_hit:
            self.player.respawn()
            self.deaths += 1
            self.total_deaths += 1
            # Reset coins
            self.coins = []
            for coin_pos in level_coins[self.current_level]:
                self.coins.append(Coin(coin_pos[0], coin_pos[1], tile_size))
            self.coins_collected = 0

        # Check for level completion
        if self.check_goal():
            if self.current_level <= len(level_data) - 1:
                self.load_level(self.current_level + 1)
            else:
                return "game_complete"

        return "playing"

    def draw_ui(self):
        # Level info with level names
        level_names = [
            "The Gauntlet",
            "Maze of Death",
            "Circle of Hell",
            "The Labyrinth",
            "Final Nightmare",
        ]

        level_text = (
            f"Level {self.current_level + 1}/5: {level_names[self.current_level]}"
        )
        level_surface = self.font.render(level_text, True, black)
        screen.blit(level_surface, (10, 10))

        # Deaths
        death_text = f"Deaths: {self.deaths} (Total: {self.total_deaths})"
        death_surface = self.font.render(death_text, True, red)
        screen.blit(death_surface, (10, 50))

        # Coins
        coin_text = f"Coins: {self.coins_collected}/{self.coins_needed}"
        coin_color = green if self.coins_collected >= self.coins_needed else red
        coin_surface = self.font.render(coin_text, True, coin_color)
        screen.blit(coin_surface, (10, 90))

        # Instructions
        if self.coins_collected < self.coins_needed:
            instruction = "Collect all coins, then reach the green zone!"
        else:
            instruction = "All coins collected! Reach the green zone!"

        instruction_surface = pygame.font.Font("freesansbold.ttf", 24).render(
            instruction, True, blue
        )
        screen.blit(instruction_surface, (10, 130))

        # Difficulty warning
        warning_text = "WARNING: This game is EXTREMELY difficult!"
        warning_surface = pygame.font.Font("freesansbold.ttf", 20).render(
            warning_text, True, red
        )
        screen.blit(warning_surface, (10, screen_height - 30))


# Main game loop
game_manager = GameManager()
run = True

while run:
    clock.tick(fps)
    screen.fill(white)

    # Update game
    game_state = game_manager.update()

    # Draw UI
    game_manager.draw_ui()

    # Check for game completion
    if game_state == "game_complete":
        # Draw completion message
        complete_text = f"LEGENDARY! You conquered the World's Hardest Game!"
        complete_surface = pygame.font.Font("freesansbold.ttf", 36).render(
            complete_text, True, green
        )
        text_rect = complete_surface.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        screen.blit(complete_surface, text_rect)

        final_text = f"Total Deaths: {game_manager.total_deaths}"
        final_surface = pygame.font.Font("freesansbold.ttf", 24).render(
            final_text, True, black
        )
        final_rect = final_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 + 50)
        )
        screen.blit(final_surface, final_rect)

        restart_text = "Press R to restart and try for fewer deaths!"
        restart_surface = pygame.font.Font("freesansbold.ttf", 20).render(
            restart_text, True, blue
        )
        restart_rect = restart_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 + 100)
        )
        screen.blit(restart_surface, restart_rect)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == "game_complete":
                # Restart game
                game_manager = GameManager()

    pygame.display.update()

pygame.quit()

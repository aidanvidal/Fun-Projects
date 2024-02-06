import numpy as np
import pygame
import random

# Initialize the grid display
pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid Display")

# Set up clock
clock = pygame.time.Clock()

# Define the color of the sand
color = (194, 178, 128)

# Define grid properties
grid_size = 10
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size

def draw_grid(grid):
    for x in range(grid_width):
        for y in range(grid_height):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            if grid[x][y] != 0:
                pygame.draw.rect(screen, (color[0], grid[x][y], color[2]), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect)
        
def init_grid():
    grid = np.zeros((grid_width, grid_height))
    return grid

def update_grid(grid, x, y):
    if x >= 0 and x < grid_width and y >= 0 and y < grid_height and grid[x][y] == 0:
        grid[x][y] = random.randint(160, 180)
    
def fall(grid):
    for x in range(grid_width):
        for y in range(grid_height-1, -1, -1):
            if grid[x][y] != 0 and y < grid_height-1 and x < grid_width-1 and x > 0 and grid[x][y+1] != 0 and grid[x+1][y+1] == 0 and grid[x-1][y+1] == 0:
                direction = random.choice([-1, 1])
                grid[x][y] = 0
                hue = random.randint(160, 180)
                grid[x+direction][y+1] = hue
            elif grid[x][y] != 0 and y < grid_height-1 and x < grid_width-1 and grid[x][y+1] != 0 and grid[x+1][y+1] == 0:
                grid[x][y] = 0
                hue = random.randint(160, 180)
                grid[x+1][y+1] = hue
            elif grid[x][y] != 0 and y < grid_height-1 and x > 0 and grid[x][y+1] != 0 and grid[x-1][y+1] == 0:
                grid[x][y] = 0
                hue = random.randint(160, 180)
                grid[x-1][y+1] = hue
            elif grid[x][y] != 0 and (y == grid_height-1 or grid[x][y+1] != 0):
                continue
            elif grid[x][y] != 0:
                grid[x][y] = 0
                hue = random.randint(160, 180)
                grid[x][y+1] = hue
    return grid

    
# Game loop
grid = init_grid() # Initialize the grid
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            # Calculate the grid position based on the mouse position
            grid_x = mouse_pos[0] // grid_size
            grid_y = mouse_pos[1] // grid_size
            # Update the grid with the new block
            update_grid(grid, grid_x, grid_y)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            # Get the position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            # Calculate the grid position based on the mouse position
            grid_x = mouse_pos[0] // grid_size
            grid_y = mouse_pos[1] // grid_size
            # Update the grid with the new block
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if random.random() < 0.60:  # 60% chance of calling update_grid
                        update_grid(grid, grid_x + i, grid_y + j)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Clear the grid
            grid = init_grid()
            

    # Update the grid
    grid = fall(grid)
    
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid(grid=grid)

    # Update the display
    clock.tick(60)
    pygame.display.flip()

# Quit the game
pygame.quit()

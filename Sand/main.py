# Sand simulation with gravity
# Uses a 2D numpy array to simulate the sand
import numpy as np
import pygame
import random

# Set Gravity
GRAVITY_ON = False

# Initialize the grid display
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Display")

# Set up clock
clock = pygame.time.Clock()
FRAME_RATE = 60

# Define the color of the sand
color = (194, 178, 128)

# Define grid properties
GRID_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

def draw_grid(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[x][y][0] != 0:
                pygame.draw.rect(screen, (color[0], grid[x][y][0], color[2]), rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect)
        
def init_grid():
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT, 2))
    return grid

def update_grid(grid, x, y):
    if x >= 0 and x < GRID_WIDTH and y >= 0 and y < GRID_HEIGHT and grid[x][y][0] == 0:
        grid[x][y][0] = random.randint(160, 180)
    
def fall_gravity(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT-1, -1, -1):
            # Determine whether the sand should fall to the left or right if there is not a block below it
            if grid[x][y][0] != 0 and y < GRID_HEIGHT-1 and grid[x][y+1][0] != 0:
                if x < GRID_WIDTH-1 and x > 0 and grid[x+1][y+1][0] == 0 and grid[x-1][y+1][0] == 0:
                    direction = random.choice([-1, 1])
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x+direction][y+1] = hue
                elif x < GRID_WIDTH-1 and grid[x+1][y+1][0] == 0:
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x+1][y+1][0] = hue
                elif x > 0 and grid[x-1][y+1][0] == 0:
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x-1][y+1][0] = hue
            elif grid[x][y][0] != 0 and (y == GRID_HEIGHT-1 or grid[x][y+1][0] != 0):
                continue
            # The sand should fall down if there is not a block below it
            elif grid[x][y][0] != 0 and y < GRID_HEIGHT-1:
                grid[x][y][0] = 0
                hue = random.randint(160, 180)
                # Determine the speed of the sand falling
                gravity = int(grid[x][y][1]/FRAME_RATE * 50)//GRID_SIZE + 1
                # If the sand has reached the bottom or there is a block below it, then stop the sand from falling
                if y+gravity >= GRID_HEIGHT or grid[x][y+gravity][0] != 0:
                    for i in range(y, GRID_HEIGHT):
                        if grid[x][i][0] != 0:
                            grid[x][i-1][0] = hue
                            grid[x][i-1][1] = 0
                            break
                        if i == GRID_HEIGHT-1:
                            grid[x][i][0] = hue
                            grid[x][i][1] = 0
                # Otherwise, continue to let the sand fall
                else:
                    grid[x][y+gravity][0] = hue
                    grid[x][y+gravity][1] = grid[x][y][1] + 1
                    grid[x][y][1] = 0
    return grid

def fall_no_gravity(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT-1, -1, -1):
            # Determine whether the sand should fall to the left or right if there is not a block below it
            if grid[x][y][0] != 0 and y < GRID_HEIGHT-1 and grid[x][y+1][0] != 0:
                if x < GRID_WIDTH-1 and x > 0 and grid[x+1][y+1][0] == 0 and grid[x-1][y+1][0] == 0:
                    direction = random.choice([-1, 1])
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x+direction][y+1] = hue
                elif x < GRID_WIDTH-1 and grid[x+1][y+1][0] == 0:
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x+1][y+1][0] = hue
                elif x > 0 and grid[x-1][y+1][0] == 0:
                    grid[x][y][0] = 0
                    hue = random.randint(160, 180)
                    grid[x-1][y+1][0] = hue
            elif grid[x][y][0] != 0 and (y == GRID_HEIGHT-1 or grid[x][y+1][0] != 0):
                continue
            # The sand should fall down if there is not a block below it
            elif grid[x][y][0] != 0 and y < GRID_HEIGHT-1:
                grid[x][y][0] = 0
                hue = random.randint(160, 180)
                grid[x][y+1][0] = hue
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
            grid_x = mouse_pos[0] // GRID_SIZE
            grid_y = mouse_pos[1] // GRID_SIZE
            # Update the grid with the new block
            update_grid(grid, grid_x, grid_y)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            # Get the position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            # Calculate the grid position based on the mouse position
            grid_x = mouse_pos[0] // GRID_SIZE
            grid_y = mouse_pos[1] // GRID_SIZE
            # Update the grid with the new block
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if random.random() < 0.60:  # 60% chance of calling update_grid
                        update_grid(grid, grid_x + i, grid_y + j)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Clear the grid
            grid = init_grid()
            

    # Update the grid
    if GRAVITY_ON:
        grid = fall_gravity(grid)
    else:
        grid = fall_no_gravity(grid)
            
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid(grid=grid)

    # Update the display
    clock.tick(FRAME_RATE)
    pygame.display.flip()

# Quit the game
pygame.quit()

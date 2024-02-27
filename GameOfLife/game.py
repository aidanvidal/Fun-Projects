# Conway's Game of Life
import pygame
import numpy as np
import time

# Initialize the game
pygame.init()

# Set the dimensions of the game window
width, height = 500, 500

# Create the game window
screen = pygame.display.set_mode((height, width))

# Create Constants
SPEED = 0.5
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRID_SIZE = 10
ROWS = width // GRID_SIZE
COLS = height // GRID_SIZE

# Create the grid
grid = np.zeros((ROWS, COLS))
live_cells = []

def update_grid():
    remove = []
    for i in range(ROWS):
        for j in range(COLS):
            # Handle the edges
            if i == 0 or j == 0 or i == ROWS - 1 or j == COLS - 1:
                continue
            total = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    total += grid[i + x, j + y]

            total -= grid[i, j]

            # Rules of the game
            if grid[i, j] == 1 and total < 2:
                live_cells.remove((i, j))
                remove.append((i, j))
            elif grid[i, j] == 1 and (total == 3 or total == 2):
                if (i, j) not in live_cells:
                    live_cells.append((i, j))
            elif grid[i, j] == 0 and total == 3:
                if (i, j) not in live_cells:
                    live_cells.append((i, j))
            elif grid[i, j] == 1 and total > 3:
                live_cells.remove((i, j))
                remove.append((i, j))
            
    for cell in live_cells:
        grid[cell[0], cell[1]] = 1
    for cell in remove:
        grid[cell[0], cell[1]] = 0

# Create the game loop
running = True
paused = False
step = False
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Click to add a cell
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            j = x // GRID_SIZE
            i = y // GRID_SIZE
            if (i, j) not in live_cells:
                live_cells.append((i, j))
                grid[i, j] = 1
            elif (i, j) in live_cells:
                live_cells.remove((i, j))
                grid[i, j] = 0
        # Press space to pause/unpause the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
        # Press right arrow to move one step
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                step = True

    if not paused or step:
        update_grid()
        step = False
        # Set a tick rate
        time.sleep(SPEED)

    for i in range(ROWS):
        for j in range(COLS):
            x = j * GRID_SIZE
            y = i * GRID_SIZE

            if grid[i, j] == 1:
                pygame.draw.rect(screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE))
    for i in range(0, width, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (i, 0), (i, width))
    for j in range(0, height, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, j), (height, j))
        
    pygame.display.update()

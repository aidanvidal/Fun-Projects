import pygame
import random

# settings
grid_size = 25
tileset_path = "WaveFunctionCollapse/tiles/demo"
random_starting_cells = 1

# Directional constants
UP = 4
DOWN = 1
LEFT = 2
RIGHT = 3
BLANK = 0

# set the screen size and cell size
screen_size = 1000
cell_size = int(screen_size // grid_size)
width, height = cell_size * grid_size, cell_size * grid_size
cols, rows = grid_size, grid_size

# rules for the tiles
rules = {
    "up": {
        BLANK: [BLANK, UP],
        DOWN: [UP, BLANK],
        LEFT: [DOWN, LEFT, RIGHT],
        RIGHT: [DOWN, LEFT, RIGHT],
        UP: [DOWN, LEFT, RIGHT]
    },
    "down": {
        BLANK: [BLANK, DOWN],
        UP: [DOWN, BLANK],
        LEFT: [UP, LEFT, RIGHT],
        RIGHT: [UP, LEFT, RIGHT],
        DOWN: [UP, LEFT, RIGHT]
    },
    "left": {
        BLANK: [BLANK, LEFT],
        RIGHT: [LEFT, BLANK],
        UP: [UP, DOWN, RIGHT],
        DOWN: [UP, DOWN, RIGHT],
        LEFT: [UP, DOWN, RIGHT]
    },
    "right": {
        BLANK: [BLANK, RIGHT],
        LEFT: [RIGHT, BLANK],
        UP: [UP, DOWN, LEFT],
        DOWN: [UP, DOWN, LEFT],
        RIGHT: [UP, DOWN, LEFT]
    }
}

# pygame setup
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("WFC")

# load the tileset
tiles = [
    pygame.image.load(f"./{tileset_path}/blank.png").convert_alpha(),
    pygame.image.load(f"./{tileset_path}/down.png").convert_alpha(),
    pygame.image.load(f"./{tileset_path}/left.png").convert_alpha(),
    pygame.image.load(f"./{tileset_path}/right.png").convert_alpha(),
    pygame.image.load(f"./{tileset_path}/up.png").convert_alpha(),
]

# lists to store the cells
cells = []
collapsed_cells = []
superposition_cells = []
cell_dict = {}

# pick cell with least entropy
def pick_cell():
    temp = superposition_cells
    sorted_cells = sorted(temp, key=lambda cell: len(cell["directions"]))
    if len(sorted_cells) > 0:
        return sorted_cells[0]
    else:
        return None

def restart_board():
    global cells, collapsed_cells, superposition_cells, cell_dict
    cells = []
    collapsed_cells = []
    superposition_cells = []
    cell_dict = {}
    init_cells()
    start_cell()
    update_directions()
    # clear the screen
    window.fill((0, 0, 0))
    pygame.display.flip()
    
# collapse the cell
def collapse(cell):
    # Check if directions are empty
    if len(cell["directions"]) == 0:
        print("No directions left")
        print("Restarting the board")
        restart_board()
        return
        
    cell["superposition"] = False
    cell["collapsed"] = True
    dir = random.choice(cell["directions"])
    cell["tile"] = tiles[dir]
    # update the direction of the cell
    cell["directions"] = [dir]
    collapsed_cells.append(cell)
    superposition_cells.remove(cell)

def get_cell(x, y):
    if (x, y) in cell_dict:
        return cell_dict[(x, y)]
    else:
        return None

# update possible directions
def update_directions():
    is_changed = False
    for cell in superposition_cells:
        x, y = cell["x"], cell["y"]
        up = get_cell(x, y - 1)
        down = get_cell(x, y + 1)
        left = get_cell(x - 1, y)
        right = get_cell(x + 1, y)
        for i in range(0,2):
            if up and up["collapsed"]:
                for d in cell["directions"]:
                    if d not in rules["down"][up["directions"][0]]:
                        cell["directions"].remove(d)
                        
            if down and down["collapsed"]:
                for d in cell["directions"]:
                    if d not in rules["up"][down["directions"][0]]:
                        cell["directions"].remove(d)
                    
            if left and left["collapsed"]:
                for d in cell["directions"]:
                    if d not in rules["right"][left["directions"][0]]:
                        cell["directions"].remove(d)
                    
            if right and right["collapsed"]:
                for d in cell["directions"]:
                    if d not in rules["left"][right["directions"][0]]:
                        cell["directions"].remove(d)
            
def init_cells():
    # create a grid of cells
    for y in range(rows):
        for x in range(cols):
            cell = {
                "x": x,
                "y": y,
                "directions": [BLANK, UP, DOWN, LEFT, RIGHT],
                "collapsed": False,
                "superposition": True,
                "tile": None,
            }
            cell_dict[(x, y)] = cell
            cells.append(cell)
            superposition_cells.append(cell)
            
def start_cell():
    # randomly collapse a cell
    for i in range(random_starting_cells):
        cell = random.choice(superposition_cells)
        cell["superposition"] = False
        cell["collapsed"] = True
        dir = random.choice(cell["directions"])  # Select a random direction from the available directions
        cell["tile"] = tiles[dir]  # Use the selected direction to get the corresponding tile
        cell["directions"] = [dir]  # Update the direction of the cell
        collapsed_cells.append(cell)
        superposition_cells.remove(cell)


init_cells()
start_cell()
update_directions()
while True:
    if len(superposition_cells) == 0:
        pygame.image.save(window, f"./WaveFunctionCollapse/output.png")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c: # Reset the board
                restart_board()
                break
            
    # draw the cells
    for cell in cells:
        if cell["collapsed"]:
            window.blit(pygame.transform.scale(cell["tile"], (cell_size, cell_size)), (cell["x"] * cell_size, cell["y"] * cell_size))
    
    '''
    #Uncommet this to and comment the thing below to be able to click to place a tile and space to get tile directions
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pick a cell and collapse it
            cell = pick_cell()
            if cell:
                collapse(cell)
                update_directions()
                update_directions()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # get the mouse position
                mouse_pos = pygame.mouse.get_pos()
                # calculate the cell coordinates
                cell_x = mouse_pos[0] // cell_size
                cell_y = mouse_pos[1] // cell_size
                # find the cell at the mouse position
                hovered_cell = None
                for cell in cells:
                    if cell["x"] == cell_x and cell["y"] == cell_y:
                        hovered_cell = cell
                        break
                # print the directions of the hovered cell
                if hovered_cell:
                    print("Directions:", hovered_cell["directions"])
        '''
        
    cell = pick_cell()
    if cell:
        collapse(cell)
        update_directions()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # update the display
    pygame.display.flip()
    clock.tick(60)


# Image to ASCII Art
import cv2
import numpy as np
import pygame

# Change to false if you want to display the ASCII art in just black and white
COLOR_WANT = True

# Density array of ASCII characters
DENSITY = 'Ñ@#W$9876543210?!abc;:+=-,._ '

# Image
IMAGE = 'test.jpg'

# Font
# If the font size is too large, the ASCII art will be too large to display
# Smaller font with larger size will make the ASCII art more clear
FONT_SIZE = 5

# Resize Values
# If the size values are too large, the ASCII art will be too large to display
WIDTH = 200
HEIGHT = 200

def get_image():
    # Read image
    image = cv2.imread(IMAGE, cv2.IMREAD_COLOR)
    # Resize image
    image = cv2.resize(image, (WIDTH, HEIGHT))
    return image

def get_brightness(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# Desnity mapping of brightness
def map_density(brightness):
    density = ''
    for i in range(WIDTH):
        for j in range(HEIGHT):
            density += DENSITY[int(brightness[i][j] / 255 * len(DENSITY)) - 1]
        density += '\n'
    return density
    
# Print ASCII art in a file
def print_ascii(density):
    with open('ascii.txt', 'w') as f:
        f.write(density)

# Display ASCII art in a new window
def display_ascii_color(density, color):
    # Set window dimensions
    window_width = WIDTH * FONT_SIZE
    window_height = HEIGHT * FONT_SIZE

    # Create a new window
    window = pygame.display.set_mode((window_width, window_height))

    # Set the window title
    pygame.display.set_caption("ASCII Art")

    # Set the font and font size
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    # Render the ASCII art
    for i, row in enumerate(density.split('\n')):
        for j, char in enumerate(row):
            rendered_ascii = font.render(char, True, color[i][j])
            window.blit(rendered_ascii, (j * FONT_SIZE, i * FONT_SIZE))

    # Blit the rendered ASCII art onto the window
    window.blit(rendered_ascii, (0, 0))
        
    # Update the display
    pygame.display.update()

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
# Display ASCII art in a new window
def display_ascii(density):
    # Set window dimensions
    window_width = WIDTH * FONT_SIZE
    window_height = HEIGHT * FONT_SIZE

    # Create a new window
    window = pygame.display.set_mode((window_width, window_height))

    # Set the window title
    pygame.display.set_caption("ASCII Art")

    # Set the font and font size
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    # Render the ASCII art
    for i, row in enumerate(density.split('\n')):
        for j, char in enumerate(row):
            rendered_ascii = font.render(char, True, (255, 255, 255))
            window.blit(rendered_ascii, (j * FONT_SIZE, i * FONT_SIZE))

    # Blit the rendered ASCII art onto the window
    window.blit(rendered_ascii, (0, 0))
        
    # Update the display
    pygame.display.update()

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    pygame.init()
    image = get_image()
    brightness = get_brightness(image)
    density = map_density(brightness)
    if COLOR_WANT:
        color = image[:, :, ::-1] # Swap blue and red channels
        display_ascii_color(density, color)
    else:
        display_ascii(density)
    print_ascii(density)
    
    
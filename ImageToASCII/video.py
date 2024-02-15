# Video to ASCII Art
import cv2
import numpy as np
import pygame

# Whether to display the ASCII art in color
COLOR_WANT = True

# Density array of ASCII characters
#DENSITY = 'Ñ@#W$9876543210?!abc;:+=-,._ '
DENSITY = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]{}?-_+~<>i!lI;:,"^`\'. '

# Font
# If the font size is too large, the ASCII art will be too large to display
# Smaller font with larger size will make the ASCII art more clear but will be delayed
FONT_SIZE = 5

# Resize Values
# If the size values are too large, the ASCII art will be too large to display
WIDTH = 150
HEIGHT = 150

def get_frame():
    # Open camera
    cap = cv2.VideoCapture(0)
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        yield frame
    # Release camera
    cap.release()

def get_brightness(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray

# Desnity mapping of brightness
def map_density(brightness):
    density = ''
    density_len = len(DENSITY)
    for i in range(WIDTH):
        for j in range(HEIGHT):
            density += DENSITY[int(brightness[i][j] / 255 * density_len) - 1]
        density += '\n'
    return density

# Display ASCII art in a new window
def display_ascii(density, window):
    # Clear the window
    window.fill((0, 0, 0))

    # Render the ASCII art
    for i, row in enumerate(density.split('\n')):
        for j, char in enumerate(row):
            rendered_ascii = font.render(char, True, (255, 255, 255))
            window.blit(rendered_ascii, (j * FONT_SIZE, i * FONT_SIZE))

    # Update the display
    pygame.display.update()

# Display ASCII art in color
def display_ascii_color(density, color, window):
    # Clear the window
    window.fill((0, 0, 0))

    # Render the ASCII art
    for i, row in enumerate(density.split('\n')):
        for j, char in enumerate(row):
            rendered_ascii = font.render(char, True, color[i][j])
            window.blit(rendered_ascii, (j * FONT_SIZE, i * FONT_SIZE))

    # Update the display
    pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    
    # Set window dimensions
    window_width = WIDTH * FONT_SIZE
    window_height = HEIGHT * FONT_SIZE

    # Create a new window
    window = pygame.display.set_mode((window_width, window_height))

    # Set the window title
    pygame.display.set_caption("ASCII Art")

    # Set the font and font size
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    if COLOR_WANT:
        for frame in get_frame():
            color = frame[:, :, ::-1]  # Swap blue and red channels
            brightness = get_brightness(frame)
            density = map_density(brightness)
            display_ascii_color(density, color, window=window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    else:
        for frame in get_frame():
            brightness = get_brightness(frame)
            density = map_density(brightness)
            display_ascii(density,window=window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


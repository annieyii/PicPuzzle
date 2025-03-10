import os
import pygame
import random
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def split_image(image, rows, cols):
    """Split the image into rows x cols smaller pieces."""
    img_width, img_height = image.get_size()
    tile_width = img_width // cols
    tile_height = img_height // rows
    tiles = [] 

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            tile = image.subsurface(rect)
            tiles.append((tile, rect))

    return tiles

def shuffle_tiles_on_screen(tiles, rows, cols, tile_width, tile_height):
    """Shuffle the puzzle pieces and randomly place them on the screen."""
    positions = []
    for row in range(rows):
        for col in range(cols):
            positions.append(pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height))
    random.shuffle(positions)

    for i, (tile, _) in enumerate(tiles):
        tiles[i] = (tile, positions[i])

def draw_grid(screen, rows, cols, tile_width, tile_height):
    """Draw a grid to assist in puzzle placement."""
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def main():
    # Use tkinter to open a file selection dialog
    Tk().withdraw()  # Hide the main tkinter window
    image_path = askopenfilename(
        title="Select an image file",
    )

    if not image_path:
        print("No image selected. Exiting program.")
        sys.exit()

    # Initialize pygame
    pygame.init()

    # Game parameters
    screen_width, screen_height = 800, 600
    rows, cols = 3, 3  # Divide the image into a 3x3 puzzle

    # Initialize the screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle Game")

    try:
        image = pygame.image.load(image_path).convert()
    except pygame.error:
        print("Failed to load the image. Please check the file.")
        pygame.quit()
        sys.exit()

    # Resize the image to fit the screen
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # Calculate individual puzzle piece size
    tile_width = screen_width // cols
    tile_height = screen_height // rows

    # Split the image into puzzle pieces and shuffle
    tiles = split_image(image, rows, cols)
    original_tiles = tiles[:]
    shuffle_tiles_on_screen(tiles, rows, cols, tile_width, tile_height)

    # Puzzle logic
    dragging = False
    selected_tile = None
    selected_index = None

    # Button parameters
    button_font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 60, 100, 40)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        # Draw the grid
        draw_grid(screen, rows, cols, tile_width, tile_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(pos):
                        if tiles == original_tiles:
                            print("Puzzle completed!")
                        else:
                            print("Puzzle is not yet completed.")
                    else:
                        for index, (_, rect) in enumerate(tiles):
                            if rect.collidepoint(pos):
                                dragging = True
                                selected_tile = tiles[index]
                                selected_index = index
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    if selected_tile:
                        _, rect = selected_tile
                        closest_row = round(rect.y / tile_height)
                        closest_col = round(rect.x / tile_width)
                        target_x = closest_col * tile_width
                        target_y = closest_row * tile_height

                        for index, (_, other_rect) in enumerate(tiles):
                            if other_rect.topleft == (target_x, target_y):
                                other_rect.x, other_rect.y = rect.x, rect.y
                                rect.x, rect.y = target_x, target_y
                                break
                        else:
                            rect.x, rect.y = target_x, target_y

            if event.type == pygame.MOUSEMOTION and dragging:
                if selected_tile:
                    _, rect = selected_tile
                    rect.x, rect.y = event.pos

        for tile, rect in tiles:
            screen.blit(tile, rect.topleft)

        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        button_text = button_font.render("Submit", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

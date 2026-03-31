import pygame
import sys

from src.settings import LEVEL_1_ABS_PATH
from src.sprites.cow import Cow
from src.sprites.duck import Duck


def main():
    # 1. Initialize Pygame
    pygame.init()

    # 2. Set up the display
    screen_width = 1280
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprite Class Test")

    # --- NEW: Load Background Image ---
    try:
        # .convert() optimizes the image format for Pygame, making drawing much faster
        background_image = pygame.image.load(LEVEL_1_ABS_PATH).convert()

        # Scale the background to ensure it perfectly fits your window dimensions
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    except FileNotFoundError:
        print("Error: Could not find 'assets/images/sprites/cow_spritesheet.png'")
        pygame.quit()
        sys.exit()

    # 3. Set up a Clock to control the frame rate
    clock = pygame.time.Clock()
    fps = 6
    
    # 4. Create the Sprite Group and instantiate the Cow and Duck
    all_sprites = pygame.sprite.Group()

    # Spawning the cow and duck in the middle of the screen
    my_cow = Cow(x=screen_width // 2, y=screen_height // 2, scale=2.5)
    my_duck = Duck(x=screen_width // 2, y=screen_height // 2, scale=2.5)

    # Add the cow and duck to the group
    all_sprites.add(my_cow)
    all_sprites.add(my_duck)

    # 5. The Main Game Loop
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Game Logic / Updating ---
        # This calls the update() method on every sprite in the group automatically
        all_sprites.update()

        # --- Rendering / Drawing ---
        # NEW: Draw the background image starting at the top-left corner (0, 0)
        screen.blit(background_image, (0, 0))

        # Draw all sprites in the group over top of the background
        all_sprites.draw(screen)

        # Update the full display Surface to the screen
        pygame.display.flip()

        # --- Frame Rate Control ---
        # Ensure the game runs at a consistent 60 frames per second
        clock.tick(fps)

    # Clean up and quit when the loop breaks
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
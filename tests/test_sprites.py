import pygame
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.settings import LEVEL_1_ABS_PATH
from src.sprites.cow import Cow
from src.sprites.duck import Duck


def main():
    pygame.init()

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprite Movement & Animation Test")

    # Load background
    try:
        background_image = pygame.image.load(LEVEL_1_ABS_PATH).convert()
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    except FileNotFoundError:
        print("Error: Could not find Level_1.png, using blank background.")
        background_image = None

    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.SysFont(None, 28)

    all_sprites = pygame.sprite.Group()

    # Spawn cow and duck at different positions so they don't overlap
    my_cow = Cow(x=screen_width // 3, y=screen_height // 2, scale=2.5)
    my_duck = Duck(x=(screen_width // 3) * 2, y=screen_height // 2, scale=2.5)

    all_sprites.add(my_cow)
    all_sprites.add(my_duck)

    running = True
    while running:
        dt = clock.tick(fps) / 1000.0

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Update ---
        all_sprites.update(dt)

        # --- Draw ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        all_sprites.draw(screen)

        # --- HUD: debug info for each sprite ---
        debug_lines = [
            "Controls: Arrow Keys = Cow | WASD = Duck | ESC = Quit",
            f"FPS: {clock.get_fps():.1f}",
            f"Cow    | pos: ({my_cow.rect.x}, {my_cow.rect.y})  dir: {my_cow.direction}  moving: {my_cow.is_moving}  frame: {int(my_cow.frame_index)}",
            f"Duck   | pos: ({my_duck.rect.x}, {my_duck.rect.y})  dir: {my_duck.direction}  moving: {my_duck.is_moving}  frame: {int(my_duck.frame_index)}",
        ]

        for i, line in enumerate(debug_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            # Draw a dark shadow behind text so it's readable over any background
            shadow_surface = font.render(line, True, (0, 0, 0))
            screen.blit(shadow_surface, (11, 11 + i * 26))
            screen.blit(text_surface, (10, 10 + i * 26))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
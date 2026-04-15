import pygame
import sys
import os

# Ensure the src directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_level import GameLevel
from src.sprites.cow import Cow
from src.sprites.duck import Duck
from src.sprites.crate import Crate
from src.sprites.button import Button
from src.sprites.fence import Fence
from src.settings import LEVEL_1_JSON_PATH, LEVEL_2_JSON_PATH


# from src.sprites.duck_key import DuckKey # Make sure to import this if needed for type checking!

def main():
    # --- Initialization ---
    pygame.init()

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("GameLevel Integration Test")

    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.SysFont(None, 28)

    # --- Load the Level ---
    json_path = LEVEL_2_JSON_PATH
    try:
        current_level = GameLevel(json_path)
    except Exception as e:
        print(f"Error loading level: {e}")
        pygame.quit()
        sys.exit()

    # --- Find Specific Sprites ---
    # We need to extract the specific actors from the level's sprite group
    # to use them in our interaction logic and HUD.
    my_cow = None
    my_duck = None
    duck_key = None
    crates = []
    fences = []
    buttons = []

    for sprite in current_level.all_sprites:
        # We use type() or isinstance() to identify the sprites
        if isinstance(sprite, Cow):
            my_cow = sprite
        elif isinstance(sprite, Duck):
            my_duck = sprite
        elif isinstance(sprite, Crate):
            crates.append(sprite)
        elif isinstance(sprite, Button):
            buttons.append(sprite)
        elif isinstance(sprite, Fence):
            fences.append(sprite)
        # Note: Replace 'type(sprite).__name__' with isinstance(sprite, DuckKey) if imported
        elif type(sprite).__name__ == "DuckKey":
            duck_key = sprite

    # State tracking
    duck_has_key = False

    # --- Main Game Loop ---
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
                # Press E to use the key after collecting it
                if event.key == pygame.K_e and duck_has_key:
                    if duck_key:
                        duck_key.kill()
                    duck_has_key = False

        # --- Update Logic ---
        # 1. Update all sprites in the level
        current_level.update(dt)

        if duck_key and duck_key.alive():
            try:
                duck_key.update(dt, my_duck)
            except TypeError:
                pass  # Failsafe in case duck_key doesn't actually take my_duck as an argument

        # 2. Cow pushes crates
        if my_cow:
            for crate in crates:
                if my_cow.rect.colliderect(crate.rect) and my_cow.is_moving:
                    push_speed = 200  # pixels per second
                    if my_cow.direction == "left":
                        crate.rect.x -= int(push_speed * dt)
                    elif my_cow.direction == "right":
                        crate.rect.x += int(push_speed * dt)
                    elif my_cow.direction == "up":
                        crate.rect.y -= int(push_speed * dt)
                    elif my_cow.direction == "down":
                        crate.rect.y += int(push_speed * dt)

        # 3. Duck collects key
        if duck_key and duck_key.alive() and not duck_key.collected and my_duck:
            if my_duck.rect.colliderect(duck_key.rect):
                duck_key.collected = True
                duck_has_key = True

        # --- Draw Logic ---
        # 1. Clear screen (fallback just in case)
        screen.fill((30, 30, 30))

        # 2. Let the level draw its background and all sprites
        current_level.draw(screen)
        current_level.draw_debug_masks(screen)

        # --- Debug Rendering ---
        # Draw hitbox rects in white
        if my_cow:
            pygame.draw.rect(screen, (255, 255, 255), my_cow.rect, 2)
        for crate in crates:
            pygame.draw.rect(screen, (255, 255, 255), crate.rect, 2)

        # --- HUD: debug info for each sprite ---
        debug_lines = [
            "Controls: Arrow Keys = Cow | WASD = Duck | ESC = Quit",
            f"FPS: {clock.get_fps():.1f}",
        ]

        if my_cow:
            debug_lines.append(
                f"Cow    | pos: ({my_cow.rect.x}, {my_cow.rect.y})  dir: {my_cow.direction}  moving: {my_cow.is_moving}  frame: {int(getattr(my_cow, 'frame_index', 0))}")
        if my_duck:
            debug_lines.append(
                f"Duck   | pos: ({my_duck.rect.x}, {my_duck.rect.y})  dir: {my_duck.direction}  moving: {my_duck.is_moving}  frame: {int(getattr(my_duck, 'frame_index', 0))}")

        debug_lines.append(f"Duck Has Key: {duck_has_key}")

        if duck_key:
            debug_lines.append(f"Key Collected: {duck_key.collected if duck_key.alive() else False}")

        # Render HUD text
        for i, line in enumerate(debug_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            shadow_surface = font.render(line, True, (0, 0, 0))
            screen.blit(shadow_surface, (11, 11 + i * 26))
            screen.blit(text_surface, (10, 10 + i * 26))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
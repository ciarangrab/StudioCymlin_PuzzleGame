import pygame
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.settings import LEVEL_1_ABS_PATH
from src.sprites.cow import Cow
from src.sprites.duck import Duck

class DuckKey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load the key spritesheet
        spritesheet_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'assets',
                'images',
                'sprites',
                'objects',
                'key_spritesheet.png'
            )
        )
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        # Slice the spritesheet into 4 frames
        self.frames = []
        frame_count = 4
        frame_width = self.spritesheet.get_width() // frame_count
        frame_height = self.spritesheet.get_height()

        for i in range(frame_count):
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
            self.frames.append(frame)

        # Animation setup
        self.frame_index = 0
        self.animation_speed = 6

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # Collection / follow state
        self.collected = False
        self.follow_offset_x = 30
        self.follow_offset_y = -20

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt, duck=None):
        self.animate(dt)

        if self.collected and duck is not None:
            self.rect.centerx = duck.rect.centerx + self.follow_offset_x
            self.rect.centery = duck.rect.centery + self.follow_offset_yg


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

    # Spawn the duck's key
    duck_key = DuckKey(x=screen_width // 2, y=screen_height // 3)
    all_sprites.add(duck_key)

    # Track whether the duck currently has the key
    duck_has_key = False

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
                #press E to use the key after collecting it
                if event.key == pygame.K_e and duck_has_key:
                    duck_key.kill()
                    duck_has_key = False

        # --- Update ---
        my_cow.update(dt)
        my_duck.update(dt)
        if duck_key.alive():
            duck_key.update(dt, my_duck)
        
        #duck collects key by touching it
        if duck_key.alive() and not duck_key.collected and my_duck.rect.colliderect(duck_key.rect):
            duck_key.collected = True
            duck_has_key = True

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
            f"Duck Has Key: {duck_has_key}",
            f"Key Collected: {duck_key.collected if duck_key.alive() else False}",
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
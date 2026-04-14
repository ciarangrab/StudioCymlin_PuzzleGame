import pygame
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.settings import LEVEL_1_ABS_PATH
from src.sprites.cow import Cow
from src.sprites.duck import Duck
from src.sprites.crate import Crate
from src.sprites.fence import Fence
from src.sprites.button import Button

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
            self.rect.centery = duck.rect.centery + self.follow_offset_y


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=2):
        super().__init__()
        
        spritesheet_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'assets',
                'images',
                'sprites',
                'objects',
                'buttons_spritesheet.png'
            )
        )
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        
        # Button dimensions: width=16, height=14
        frame_width = 20
        frame_height = 14
        frame_count = self.spritesheet.get_width() // frame_width
        
        # Extract all frames
        self.frames = []
        for i in range(frame_count):
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)
        
        # Animation setup
        self.frame_index = 0
        self.animation_speed = 8  # frames per second
        self.frame_timer = 0
        self.crate_touching = False
        self.was_touching = False
        self.animating = False
        self.animation_direction = 1  # 1 for forward, -1 for backward
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def animate(self, dt):
        if self.animating:
            # Track time until next frame
            self.frame_timer += dt
            frame_duration = 1.0 / self.animation_speed  # Time per frame
            
            if self.frame_timer >= frame_duration:
                self.frame_timer = 0
                self.frame_index += self.animation_direction
                
                # Check bounds and stop animation
                if self.animation_direction == 1:  # Forward
                    if self.frame_index >= len(self.frames) - 1:
                        self.frame_index = len(self.frames) - 1
                        self.animating = False
                else:  # Backward
                    if self.frame_index <= 0:
                        self.frame_index = 0
                        self.animating = False
            
            self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)



def main():
    pygame.init()

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprite Movement & Animation Test")

    # Load level data from JSON
    level_json_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'levels',
            'level1.json'
        )
    )
    with open(level_json_path, 'r') as f:
        level_data = json.load(f)

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
    
    # Spawn a button
    button_pos = level_data.get("buttons_start", [[600, 200]])[0]
    button = Button(x=button_pos[0], y=button_pos[1], scale=2)
    all_sprites.add(button)

    # Spawn a crate
    crate_data = level_data.get("crates_start", [{"position": [640, 400], "locked": False}])[0]
    if isinstance(crate_data, dict):
        crate_pos = crate_data.get("position", [640, 400])
        locked = crate_data.get("locked", False)
        my_crate = Crate(x=crate_pos[0], y=crate_pos[1], scale=1.3, locked=locked)
    else:
        # Old format: just coordinates
        my_crate = Crate(x=crate_data[0], y=crate_data[1], scale=1.3)
    all_sprites.add(my_crate)

    my_cow = Cow(x=21, y=375, scale=2)
    all_sprites.add(my_cow)

    # Spawn a fence
    fence_pos = level_data.get("fences_start", [[700, 300]])[0]
    fence = Fence(x=fence_pos[0], y=fence_pos[1], scale=2)
    all_sprites.add(fence)

    my_duck = Duck(x=1015, y=500, scale=2)
    all_sprites.add(my_duck)

    # Spawn the duck's key
    duck_key = DuckKey(x=890, y=330)
    all_sprites.add(duck_key)

    # Create a collision handler for the cow to check fence collisions
    class CollisionHandler:
        def __init__(self, fence):
            self.fences = [fence]
        
        def check_fence_collision(self, sprite):
            """Check if sprite collides with any visible fence"""
            for fence in self.fences:
                # Only check collision with visible fences (frame_index > 0)
                if fence.frame_index > 0:
                    if sprite.rect.colliderect(fence.rect):
                        return True
            return False
        
        def check_wall_collision(self, sprite):
            """No wall collision check needed in test mode"""
            return False
    
    collision_handler = CollisionHandler(fence)

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
        my_cow.update(dt, collision_handler)
        my_duck.update(dt)
        if duck_key.alive():
            duck_key.update(dt, my_duck)
        
        # Cow pushes crate (only if crate is not locked)
        if my_cow.rect.colliderect(my_crate.rect) and my_cow.is_moving and not my_crate.locked:
            push_speed = 200  # pixels per second
            if my_cow.direction == "left":
                my_crate.rect.x -= int(push_speed * dt)
            elif my_cow.direction == "right":
                my_crate.rect.x += int(push_speed * dt)
            elif my_cow.direction == "up":
                my_crate.rect.y -= int(push_speed * dt)
            elif my_cow.direction == "down":
                my_crate.rect.y += int(push_speed * dt)
        
        # Key touches locked crate: unlock it and consume the key
        if duck_key.alive() and my_crate.locked and duck_key.rect.colliderect(my_crate.rect):
            my_crate.unlock()
            duck_key.kill()
        
        # Check if crate is touching button
        if my_crate.rect.colliderect(button.rect):
            if not button.was_touching:
                # Crate just started touching: play forward animation
                button.was_touching = True
                button.animating = True
                button.animation_direction = 1
            # Crate touching: fence animates backwards
            if not fence.animating:
                fence.animating = True
                fence.animation_direction = -1
        else:
            if button.was_touching:
                # Crate just stopped touching: play backward animation
                button.was_touching = False
                button.animating = True
                button.animation_direction = -1
            # Crate not touching: fence animates forwards (unless already at last frame)
            if fence.frame_index < len(fence.frames) - 1:
                if not fence.animating:
                    fence.animating = True
                    fence.animation_direction = 1
        
        # Update button animation
        button.update(dt)
        
        #duck collects key by touching it
        if duck_key.alive() and not duck_key.collected and my_duck.rect.colliderect(duck_key.rect):
            duck_key.collected = True
            duck_has_key = True

        # Update fence animation
        fence.update(dt)

        # --- Draw ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        all_sprites.draw(screen)

        # --- Debug: Draw hitbox rects in white ---
        pygame.draw.rect(screen, (255, 255, 255), my_cow.rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), my_crate.rect, 2)

        # --- HUD: debug info for each sprite ---
        debug_lines = [
            "Controls: Arrow Keys = Cow | WASD = Duck | ESC = Quit",
            f"FPS: {clock.get_fps():.1f}",
            f"Cow    | pos: ({my_cow.rect.x}, {my_cow.rect.y})  dir: {my_cow.direction}  moving: {my_cow.is_moving}  frame: {int(my_cow.frame_index)}",
            f"Duck   | pos: ({my_duck.rect.x}, {my_duck.rect.y})  dir: {my_duck.direction}  moving: {my_duck.is_moving}  frame: {int(my_duck.frame_index)}",
            f"Crate  | pos: ({my_crate.rect.x}, {my_crate.rect.y})  locked: {my_crate.locked}",
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
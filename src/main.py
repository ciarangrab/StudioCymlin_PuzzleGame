import pygame
import sys
import os
from PIL import Image

# Ensure the src directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game_level import GameLevel
from src.sprites.cow import Cow
from src.sprites.duck import Duck
from src.sprites.crate import Crate
from src.sprites.button import Button
from src.sprites.fence import Fence
from src.settings import LEVEL_1_JSON_PATH, LEVEL_2_JSON_PATH, LEVEL_3_JSON_PATH, TITLE_SCRN_ABS_PATH, CUTSCENE_1_ABS_PATH, END_SCRN_ABS_PATH


def load_apng_frames(filepath, scale=4):
    """ Loads an animated PNG, extracts the frames, and scales them """
    try:
        pil_image = Image.open(filepath)
    except IOError:
        print(f"Error: Could not load image at {filepath}")
        return []
    
    frames = []

    # Extract the frames, convert to rbga, and scale
    for frame_index in range(pil_image.n_frames):
        pil_image.seek(frame_index)
        frame_rgba = pil_image.convert("RGBA")
        raw_str = frame_rgba.tobytes("raw", "RGBA")

        pygame_surface = pygame.image.frombytes(raw_str, frame_rgba.size, "RGBA")
        
        if scale != 1:
            new_width = int(pygame_surface.get_width() * scale)
            new_height = int(pygame_surface.get_height() * scale)
            pygame_surface = pygame.transform.scale(pygame_surface, (new_width, new_height))
            
        duration = pil_image.info.get('duration', 100) 
        frames.append({
            'surface': pygame_surface,
            'duration': duration
        })
        
    return frames


def play_cutscene(screen, clock, apng_frames, fps, screen_width, screen_height, sceneId=0):
    """ Plays an animaged PNG cutscene loop until it finishes or the player skips it """

    if not apng_frames:
            return # Skip if frames failed to load

    current_frame_index = 0
    time_since_last_frame = 0
    cutscene_running = True

    while cutscene_running:
        dt = clock.tick(fps)
        
        # Event handling for the cutscene
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if sceneId == 0:
                    # If sceneId is 0 --> ANY key press ends the loop
                    cutscene_running = False
                else:
                    # Otherwise, only specific keys skip the cutscene
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                        cutscene_running = False
            
            # Optional: Allow mouse clicks to skip if sceneId == 0
            if event.type == pygame.MOUSEBUTTONDOWN and sceneId == 0:
                cutscene_running = False
                    
        if not cutscene_running:
            break 

        # Cutscene Animation Logic
        time_since_last_frame += dt
        current_duration = apng_frames[current_frame_index]['duration']

        if time_since_last_frame >= current_duration:
            time_since_last_frame = 0 
            if current_frame_index < len(apng_frames) - 1:
                current_frame_index += 1
            else:
                # Reached the end of the frames
                if sceneId == 0:
                    current_frame_index = 0 # Loop back to the first frame
                else:
                    cutscene_running = False # Animation finished normally

        # Draw Cutscene
        screen.fill((30, 30, 30)) 
        current_surface = apng_frames[current_frame_index]['surface']
        x_pos = (screen_width - current_surface.get_width()) // 2
        y_pos = (screen_height - current_surface.get_height()) // 2
        screen.blit(current_surface, (x_pos, y_pos)) 
        
        pygame.display.flip()


def load_level(json_path):
    """ Instantiates a game level"""
    level = GameLevel(json_path)
    my_cow, my_duck, duck_key = None, None, None
    crates, fences, buttons = [], [], []

    # Find specific sprites
    # We need to extract the specific actors from the level's sprite group
    # to use them in our interaction logic and HUD.
    for sprite in level.all_sprites:
        if isinstance(sprite, Cow): my_cow = sprite
        elif isinstance(sprite, Duck): my_duck = sprite
        elif isinstance(sprite, Crate): crates.append(sprite)
        elif isinstance(sprite, Button): buttons.append(sprite)
        elif isinstance(sprite, Fence): fences.append(sprite)
        elif type(sprite).__name__ == "DuckKey": duck_key = sprite

    return level, my_cow, my_duck, duck_key, crates, fences, buttons



# from src.sprites.duck_key import DuckKey

def main():
    # Initialization 
    pygame.init()
    pygame.mixer.init() 

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pushy Farm")

    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.SysFont(None, 28)
    
    # Load cutscene frames
    title_frames = load_apng_frames(TITLE_SCRN_ABS_PATH, scale=4)           # Title Screen
    cutscene_1_frames = load_apng_frames(CUTSCENE_1_ABS_PATH, scale=4)      # Opening Sequence
    end_frames = load_apng_frames(END_SCRN_ABS_PATH, scale=4)               # End Screen

    # Play Title Screen
    play_cutscene(screen, clock, title_frames, fps, screen_width, screen_height, sceneId=0)

    # Play intro cutscene
    play_cutscene(screen, clock, cutscene_1_frames, fps, screen_width, screen_height, sceneId=1)


    # Setup for sprites
    my_cow = None
    my_duck = None
    duck_key = None
    crates = []
    fences = []
    buttons = []

    # Load the level
    level_paths = [LEVEL_1_JSON_PATH, LEVEL_2_JSON_PATH, LEVEL_3_JSON_PATH]
    current_level_index = 0
    current_level, my_cow, my_duck, duck_key, crates, fences, buttons = load_level(level_paths[current_level_index])
    duck_has_key = False

    # State tracking
    duck_has_key = False

    # Main game loop 
    running = True
    while running:
        dt = clock.tick(fps) / 1000.0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    current_level, my_cow, my_duck, duck_key, crates, fences, buttons = load_level(level_paths[current_level_index])
                    duck_has_key = False

        # Update all sprites in the level
        current_level.update(dt)

        # Level switch, cow walks off the right edge
        if my_cow and my_cow.rect.left > 1280:
            current_level_index += 1
            if current_level_index < len(level_paths):
                current_level, my_cow, my_duck, duck_key, crates, fences, buttons = load_level(level_paths[current_level_index])
                duck_has_key = False
            else:
                print("All levels complete!")
                running = False

        if duck_key and duck_key.alive():
            try:
                duck_key.update(dt, my_duck)
            except TypeError:
                pass  # Failsafe in case duck_key doesn't actually take my_duck as an argument

        #  Crate Logic
        if my_cow:
            for crate in crates:
                # Crate collision 
                if my_cow.rect.colliderect(crate.rect) and my_cow.is_moving:
                    
                    # Check if the crate is locked, if it is you can't push it
                    if crate.locked:
                        # Snap the cow to the edge of the locked crate so the cow doesn't clip
                        if my_cow.direction == "left":
                            my_cow.rect.left = crate.rect.right
                        elif my_cow.direction == "right":
                            my_cow.rect.right = crate.rect.left
                        elif my_cow.direction == "up":
                            my_cow.rect.top = crate.rect.bottom
                        elif my_cow.direction == "down":
                            my_cow.rect.bottom = crate.rect.top
                            
                        # Keep the cow's raw coordinates synced
                        my_cow.x = my_cow.rect.x
                        my_cow.y = my_cow.rect.y
                        
                        break # Stop checking this crate since we can't push it

                    # Save crate's starting position before modifying
                    old_crate_x = crate.rect.x
                    old_crate_y = crate.rect.y
                    
                    # SNAP the crate to the cow to completely remove the clip/overlap
                    if my_cow.direction == "left":
                        crate.rect.right = my_cow.rect.left
                    elif my_cow.direction == "right":
                        crate.rect.left = my_cow.rect.right
                    elif my_cow.direction == "up":
                        crate.rect.bottom = my_cow.rect.top
                    elif my_cow.direction == "down":
                        crate.rect.top = my_cow.rect.bottom
                        
                    # Check if the newly snapped crate hits ANOTHER crate
                    hit_crate = any(crate != other_crate and crate.rect.colliderect(other_crate.rect) for other_crate in crates)
                    
                    # Check if the crate hits a WALL or FENCE
                    hit_wall = current_level.check_wall_collision(crate) or current_level.check_fence_collision(crate)

                    # If the crate is blocked, BOTH objects must stop
                    if hit_crate or hit_wall:
                        # Revert the crate to where it was
                        crate.rect.x = old_crate_x
                        crate.rect.y = old_crate_y
                        
                        # Snap the cow to the edge of the blocked crate so the cow doesn't clip
                        if my_cow.direction == "left":
                            my_cow.rect.left = crate.rect.right
                        elif my_cow.direction == "right":
                            my_cow.rect.right = crate.rect.left
                        elif my_cow.direction == "up":
                            my_cow.rect.top = crate.rect.bottom
                        elif my_cow.direction == "down":
                            my_cow.rect.bottom = crate.rect.top
                            
                        # Keep the cow's raw coordinates synced to its rect
                        my_cow.x = my_cow.rect.x
                        my_cow.y = my_cow.rect.y
                        
                        break # We hit an obstacle, stop checking this crate
                
                # Key touches locked crate: unlock it and consume the key
                if duck_key.alive() and crate.locked and duck_key.rect.colliderect(crate.rect):
                    crate.unlock()
                    duck_key.kill()

        # Handle Button and Fence Logic
        for button in current_level.buttons:
            
            # Check if the cow or any crate in the list of crates is touching this specific button
            is_pressed = any(crate.rect.colliderect(button.rect) for crate in crates) or my_cow.rect.colliderect(button.rect)

            if is_pressed:
                if not button.was_touching:
                    # Object just started touching: play forward animation
                    button.was_touching = True
                    button.animating = True
                    button.animation_direction = 1
                
                # Check if this button actually has a fence linked to it
                if hasattr(button, 'target_fence') and button.target_fence is not None:
                    linked_fence = button.target_fence
                    
                    # Object touching: fence animates backwards (opens)
                    if not linked_fence.animating:
                        linked_fence.animating = True
                        linked_fence.animation_direction = -1
                        
            else:
                if button.was_touching:
                    # Object just stopped touching: play backward animation
                    button.was_touching = False
                    button.animating = True
                    button.animation_direction = -1
                
                # Check if this button actually has a fence linked to it
                if hasattr(button, 'target_fence') and button.target_fence is not None:
                    linked_fence = button.target_fence
                    
                    # Object not touching: fence animates forwards (unless already at last frame)
                    if linked_fence.frame_index < len(linked_fence.frames) - 1:
                        if not linked_fence.animating:
                            linked_fence.animating = True
                            linked_fence.animation_direction = 1
                

        # Duck collects key
        if duck_key and duck_key.alive() and not duck_key.collected and my_duck:
            if my_duck.rect.colliderect(duck_key.rect):
                duck_key.collected = True
                duck_has_key = True

      
        #  Clear screen (fallback just in case)
        screen.fill((30, 30, 30))

        #  Let the level draw its background and all sprites
        current_level.draw(screen)

        # debug info for each sprite 
        debug_lines = [
            "Controls: Arrow Keys = Cow | WASD = Duck | R = Restart | ESC = Quit",
            f"FPS: {clock.get_fps():.1f}",
        ]

        # Render HUD text
        for i, line in enumerate(debug_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            shadow_surface = font.render(line, True, (0, 0, 0))
            screen.blit(shadow_surface, (11, 11 + i * 26))
            screen.blit(text_surface, (10, 10 + i * 26))

        pygame.display.flip()
    
    # Play Ending Cutscene
    play_cutscene(screen, clock, end_frames, fps, screen_width, screen_height, sceneId=1)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
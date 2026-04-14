import pygame
import json

from src.settings import LEVELS_DIR, COLLISION_MASK_DIR
from src.sprites.cow import Cow
from src.sprites.duck import Duck
from src.sprites.crate import Crate
from src.sprites.fence import Fence
from src.sprites.button import Button
from tests.test_sprites import DuckKey

class GameLevel:

    def __init__(self, json_filepath):
        """
        Loads specific level data from the level JSON file, sets the background and collision mask, and loads sprites
        to their starting positions
        """

        # Read level data from json file
        with open(json_filepath, 'r') as file:
            level_data = json.load(file)

        # Get file paths for the level from level json file
        bg_path = LEVELS_DIR / level_data["background_image"]
        mask_path  = COLLISION_MASK_DIR / level_data["collision_mask"]

        # Get sprite starting positions from level json file
        self.cow_start_pos = level_data.get("cow_start", [0,0])
        self.duck_start_pos = level_data.get("duck_start", [0,0])
        self.key_start_pos = level_data.get("key_start", [0,0])
        self.buttons_start_pos = level_data.get("buttons_start", [[0,0]])
        self.crates_start_pos = level_data.get("crates_start", [{"position": [0,0], "locked": False}])
        self.fences_start_pos = level_data.get("fences_start", [[0,0]])

        # Load the level background
        self.background_image = pygame.image.load(str(bg_path)).convert()
        self.background_image = pygame.transform.scale(self.background_image, (1280, 720))
        self.rect = self.background_image.get_rect(topleft=(0,0))

        # Load the collision mask image
        mask_surface = pygame.image.load(str(mask_path)).convert()
        mask_surface = pygame.transform.scale(mask_surface, (1280, 720))


        # Set collision mask
        self.mask = pygame.mask.from_threshold(mask_surface, pygame.Color('white'), (10, 10, 10, 255))


        # ---- Load Sprites ----
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()

        # --- Object Sprites ---
        # -- Key --
        duck_key = DuckKey(self.key_start_pos[0], self.key_start_pos[1])
        self.all_sprites.add(duck_key)

        # -- Crates --
        for crate_data in self.crates_start_pos:
            # Handle both old format [x, y] and new format with {"position": [x, y], "locked": bool}
            if isinstance(crate_data, dict):
                x, y = crate_data.get("position", [0, 0])
                locked = crate_data.get("locked", False)
                crate = Crate(x=x, y=y, scale=2, locked=locked)
            else:
                # Old format: just coordinates
                crate = Crate(x=crate_data[0], y=crate_data[1], scale=2)
            self.all_sprites.add(crate)

        # -- Fences --
        self.fences = []
        for fence_pos in self.fences_start_pos:
            fence = Fence(x=fence_pos[0], y=fence_pos[1], scale=2)
            self.all_sprites.add(fence)
            self.fences.append(fence)

        # -- Buttons --
        # TODO Add in for loop to load buttons after creating button class
        self.buttons = []
        for button_pos in self.buttons_start_pos:
            button = Button(x=button_pos[0], y=button_pos[1], scale=2)
            self.all_sprites.add(button)
            self.buttons.append(button)

        # --- Character Sprites ---
        # -- Cow --
        cow = Cow(x=self.cow_start_pos[0], y=self.cow_start_pos[1], scale=2)
        self.all_sprites.add(cow)

        # -- Duck --
        duck = Duck(x=self.duck_start_pos[0], y=self.duck_start_pos[1], scale=2)
        self.all_sprites.add(duck)

    def update(self, dt=1):
        """ Updates all sprites in the level """
        self.all_sprites.update(dt, self)

    def draw(self, surface):
        """ Draws images to the screen """

        # Draw the background image
        surface.blit(self.background_image, self.rect)

        # Draw the sprites
        self.all_sprites.draw(surface)

    def check_wall_collision(self, sprite):
        """ Returns True if the sprite overlaps a wall --> white pixels on the collision mask """

        # Compare sprite mask against level mask
        if not hasattr(sprite, 'mask'):
            sprite.mask = pygame.mask.from_surface(sprite.image)

        # Calculate offset
        offset_x = sprite.rect.x - self.rect.x
        offset_y = sprite.rect.y - self.rect.y

        # Check for overlap --> anything other than None means a collision with the wall
        return self.mask.overlap(sprite.mask, (offset_x, offset_y)) is not None

    def check_fence_collision(self, sprite):
        """ Returns True if the sprite collides with any visible fence """
        for fence in self.fences:
            # Only check collision with visible fences (frame_index > 0)
            if fence.frame_index > 0:
                if sprite.rect.colliderect(fence.rect):
                    return True
        return False

    def draw_debug_masks(self, surface):
        """ Renders the invisible collision data to the screen. Walls = Red, Sprites = Blue """

        # 1. Paint the level's wall mask RED
        if hasattr(self, 'mask'):
            # setcolor is the solid part, unsetcolor is the transparent part
            wall_surface = self.mask.to_surface(setcolor=(255, 0, 0, 150), unsetcolor=(0, 0, 0, 0))
            surface.blit(wall_surface, self.rect)

        # 2. Paint the sprites' masks BLUE
        for sprite in self.all_sprites:
            if hasattr(sprite, 'mask'):
                sprite_surface = sprite.mask.to_surface(setcolor=(0, 0, 255, 150), unsetcolor=(0, 0, 0, 0))
                surface.blit(sprite_surface, sprite.rect)
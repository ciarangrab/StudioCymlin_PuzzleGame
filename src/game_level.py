import pygame
import json

from src.settings import LEVELS_DIR, COLLISION_MASK_DIR
from src.sprites.cow import Cow
from src.sprites.duck import Duck
from src.sprites.crate import Crate
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
        self.buttons_start_pos = level_data.get("buttons_start", [[], []])
        self.crates_start_pos = level_data.get("crates_start", [[], []])

        # Load the level background
        self.background_image = pygame.image.load(str(bg_path)).convert()
        self.rect = self.background_image.get_rect(topleft=(0,0))

        # Load the collision mask image
        mask_surface = pygame.image.load(str(mask_path)).convert()
        mask_surface.set_colorkey((0, 0, 0))

        # Set collision mask
        self.mask = pygame.mask.from_surface(mask_surface)


        # ---- Load Sprites ----
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()

        # --- Object Sprites ---
        # -- Key --
        duck_key = DuckKey(self.key_start_pos[0], self.key_start_pos[1])
        self.all_sprites.add(duck_key)

        # -- Crates --
        for crates in self.crates_start_pos:
            crate = Crate(x=crates[0], y=crates[1], scale=2)
            self.all_sprites.add(crate)

        # -- Buttons --
        # TODO Add in for loop to load buttons after creating button class

        # --- Character Sprites ---
        # -- Cow --
        cow = Cow(x=self.cow_start_pos[0], y=self.cow_start_pos[1], scale=2)
        self.all_sprites.add(cow)

        # -- Duck --
        duck = Duck(x=self.duck_start_pos[0], y=self.duck_start_pos[1], scale=2)
        self.all_sprites.add(duck)

    def update(self, dt=1):
        """ Updates all sprites in the level """
        self.all_sprites.update(dt)

    def draw(self, surface):
        """ Draws images to the screen """

        # Draw the background image
        surface.blit(self.background_image, self.rect)

        # Draw the sprites
        self.all_sprites.draw(surface)
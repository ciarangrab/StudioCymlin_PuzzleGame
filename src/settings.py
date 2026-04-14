import os 
import pathlib
import pygame

# Absolute Path to the settings file
SETTINGS_ROOT = pathlib.Path(__file__).resolve()

# Path to the project root
PROJECT_ROOT = SETTINGS_ROOT.parent.parent

# Path Constants for the folders
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
COLLISION_MASK_DIR = IMAGES_DIR / 'collision_masks'
SPRITES_DIR = IMAGES_DIR / "sprites"
OBJECTS_DIR = SPRITES_DIR / "objects"
LEVELS_DIR = IMAGES_DIR / "levels"

JSON_LEVELS_DIR = PROJECT_ROOT / "levels"

# ---- Absolute Paths for core files -----

# Sprites 
COW_SPRITESHEET_ABS_PATH = str(SPRITES_DIR / "cow_spritesheet.png")
DUCK_SPRITESHEET_ABS_PATH = str(SPRITES_DIR / "duck_spritesheet.png")

# Objects
CRATE_SPRITESHEET_ABS_PATH = str(OBJECTS_DIR / "crate_spritesheet.png")
KEY_SPRITESHEET_ABS_PATH = str(OBJECTS_DIR / "key_spritesheet.png")
BUTTON_SPRITESHEET_ABS_PATH = str(OBJECTS_DIR/ "buttons_spritesheet.png")

# Level 1
LEVEL_1_JSON_PATH = str(JSON_LEVELS_DIR / "level1.json")
LEVEL_1_ABS_PATH = str(LEVELS_DIR / "Level_1.png")
LEVEL_1_COLL_MASK = str(COLLISION_MASK_DIR / "Level_1_Collision_Mask.png")

# Level 2
LEVEL_2_JSON_PATH = str(JSON_LEVELS_DIR / "level2.json")
LEVEL_2_ABS_PATH = str(LEVELS_DIR / "Level_2.png")
LEVEL_2_COLL_MASK = str(COLLISION_MASK_DIR / "Level_2_Collision_Mask.png")
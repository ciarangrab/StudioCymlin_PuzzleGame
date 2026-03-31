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
SPRITES_DIR = IMAGES_DIR / "sprites"
LEVELS_DIR = IMAGES_DIR / "levels"

# Absolute Paths for core files
COW_SPRITESHEET_ABS_PATH = str(SPRITES_DIR / "cow_spritesheet.png")
LEVEL_1_ABS_PATH = str(LEVELS_DIR / "Level_1.png")
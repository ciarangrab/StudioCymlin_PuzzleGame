import pygame

from src.settings import CRATE_SPRITESHEET_ABS_PATH
from src.sprites.game_sprite import GameSprite


class Crate(GameSprite):
    def __init__(self, x: int, y: int, scale: int = 1, locked: bool = False):
        """Extract crate frames from the crate spritesheet (27x32 cells).
        
        Args:
            x: X position
            y: Y position
            scale: Scale factor for the sprite
            locked: If True, displays as frame 2 (locked state)
        """

        super().__init__(scale)
        
        self.locked = locked

        try:
            self.sprite_sheet = pygame.image.load(CRATE_SPRITESHEET_ABS_PATH)
        except FileNotFoundError:
            print("Error: Could not find 'assets/images/sprites/objects/crate_spritesheet.png'")
            return
        
        try:
            self.sound = pygame.mixer.Sound("assets/images/sfx/unlock.mp3")
            self.sound.set_volume(1)
        except FileNotFoundError:
            print("Error: Could not find unlock sound")
            self.sound = None

        sprite_width = 27
        sprite_height = 27
        sheet_width = self.sprite_sheet.get_width()
        frame_count = sheet_width // sprite_width

        # Store all frames; this is a non-moving object so we reuse `walk_right_frames`.
        for i in range(frame_count):
            frame = self.get_image(
                x=i * sprite_width,
                y=0,
                width=sprite_width,
                height=sprite_height,
                scale=scale,
            )
            self.walk_right_frames.append(frame)
            self.walk_left_frames.append(frame)  # static object same in both directions

        # Fallback: if no frames were extracted, create a transparent placeholder
        if not self.walk_right_frames:
            self.image = pygame.Surface((sprite_width * scale, sprite_height * scale), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
        else:
            # If locked, show frame 2; otherwise show frame 0
            frame_index = 2 if self.locked and len(self.walk_right_frames) > 2 else 0
            self.image = self.walk_right_frames[frame_index]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def unlock(self):
        """Unlock the crate and update visual representation."""
        self.locked = False
        if self.sound:
            self.sound.play()
        if len(self.walk_right_frames) > 0:
            self.image = self.walk_right_frames[0]

    def get_all_frames(self):
        """Return a list of all extracted crate animation frames."""
        return list(self.walk_right_frames)

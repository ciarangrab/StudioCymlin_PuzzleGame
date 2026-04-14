import pygame

from src.settings import KEY_SPRITESHEET_ABS_PATH
from src.sprites.game_sprite import GameSprite


class Key(GameSprite):
    def __init__(self, x: int, y: int, scale: int = 1):
        """Extract key frames from the key spritesheet."""

        super().__init__(scale)

        try:
            self.sprite_sheet = pygame.image.load(KEY_SPRITESHEET_ABS_PATH)
        except FileNotFoundError:
            print("Error: Could not find 'assets/images/sprites/objects/key_spritesheet.png'")
            return

        sheet_width = self.sprite_sheet.get_width()
        sprite_height = self.sprite_sheet.get_height()
        frame_count = 4  # Key has 4 frames
        sprite_width = sheet_width // frame_count

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
            self.image = self.walk_right_frames[0]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def get_all_frames(self):
        """Return a list of all extracted key animation frames."""
        return list(self.walk_right_frames)

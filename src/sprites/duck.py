import pygame

from src.settings import COW_SPRITESHEET_ABS_PATH
from src.sprites.game_sprite import GameSprite

class Duck(GameSprite):
    def __init__(self, x, y, scale):
        """
        Goes through the frames of the duck sprite sheet given its dimensions and saves
        the images of each frame to the frame arrays for the cow sprite instance
        """

        super().__init__(scale)

        # Set sprite sheet image
        try:
            self.sprite_sheet = pygame.image.load(COW_SPRITESHEET_ABS_PATH)  # FIXME: Get correct duck sprite sheet addr
        except FileNotFoundError:
            print("Error: Could not find 'assets/images/sprites/cow_spritesheet.png'")
            return

        for i in range(4):      #FIXME: Update the x and y values for sprite sheet dimensions
            # Row 1 (Right): X moves by [   ] pixels each loop
            self.walk_right_frames.append(self.get_image(x=i * 37, y=0, width=37, height=30, scale=scale))

            # Row 1 (Left): Same as above, but flipped
            self.walk_left_frames.append(
                self.get_image(x=i * 37, y=0, width=37, height=30, scale=scale, flip_x=True))

            # Row 2 (Down): X moves by [   ] pixels each loop
            self.walk_down_frames.append(self.get_image(x=i * 25, y=30, width=25, height=36, scale=scale))

            # Row 3 (Up): X moves by [   ] pixels each loop
            self.walk_up_frames.append(self.get_image(x=i * 25, y=66, width=25, height=34, scale=scale))

        # Set a starting image for the sprite [Default to walking right]
        self.image = self.walk_right_frames[0]

        # Set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        """ Handles Player info for animation """

        # Get the keys that are currently being pressed
        keys = pygame.key.get_pressed()

        # Reset movement for movement check
        self.is_moving = False

        # Determine Movement Direction
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            self.is_moving = True

        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            self.is_moving = True

        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = "up"
            self.is_moving = True

        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = "down"
            self.is_moving = True

        super().update()
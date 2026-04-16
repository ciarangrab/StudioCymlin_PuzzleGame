import pygame

from src.settings import COW_SPRITESHEET_ABS_PATH
from src.sprites.game_sprite import GameSprite


class Cow(GameSprite):
    def __init__(self, x, y, scale):

        """
        Goes through the frames of the cow sprite sheet given its dimensions and saves the
        images of each frame to the frame arrays for the cow sprite instance
        """

        super().__init__(scale)

        self.spriteID = 0
        self.walk_sound_playing = False

        # Set sprite sheet image
        try:
            self.sprite_sheet = pygame.image.load(COW_SPRITESHEET_ABS_PATH)
        except FileNotFoundError:
            print("Error: Could not find 'assets/images/sprites/cow_spritesheet.png'")
            return

        try:
            self.walk_sound = pygame.mixer.Sound("assets/images/sfx/cow_walk.mp3")
            self.walk_sound.set_volume(4)
        except FileNotFoundError:
            print("Error: Could not find cow walk sound")
            self.walk_sound = None


        # Extract all frames
        for i in range(4):
            # Row 1 (Right): X moves by 37 pixels each loop
            self.walk_right_frames.append(self.get_image(x=i * 37, y=0, width=37, height=30, scale=scale))

            # Row 1 (Left): Same as above but flipped
            self.walk_left_frames.append(
                self.get_image(x=i * 37, y=0, width=37, height=30, scale=scale, flip_x=True))

            # Row 2 (Down): X moves by 25 pixels each loop
            self.walk_down_frames.append(self.get_image(x=i * 25, y=30, width=25, height=36, scale=scale))

            # Row 3 (Up): X moves by 25 pixels each loop
            self.walk_up_frames.append(self.get_image(x=i * 25, y=66, width=25, height=34, scale=scale))

        # Set a starting image for the sprite [Default to walking right]
        self.image = self.walk_right_frames[0]

        # Set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, dt=1, level=None):
        """ Handles Player info for animation """

        PIXELS_PER_SECOND = 200

        # Get the keys that are currently being pressed
        keys = pygame.key.get_pressed()

        # Reset movement for movement check
        self.is_moving = False

        # ---- Movement and Collision ----
        # [ Cow movement controlled by arrow keys ]
        # Only one direction allowed per frame (no diagonal movement, like duck)

        if keys[pygame.K_LEFT]:
            self.x = self.rect.x
            self.rect.x -= int(PIXELS_PER_SECOND * dt)
            self.direction = "left"
            self.is_moving = True
            
            # Check for x-axis collisions
            if level and (level.check_wall_collision(self) or level.check_fence_collision(self)):
                self.rect.x = self.x

        elif keys[pygame.K_RIGHT]:
            self.x = self.rect.x
            self.rect.x += int(PIXELS_PER_SECOND * dt)
            self.direction = "right"
            self.is_moving = True
            
            # Check for x-axis collisions
            if level and (level.check_wall_collision(self) or level.check_fence_collision(self)):
                self.rect.x = self.x

        elif keys[pygame.K_UP]:
            self.y = self.rect.y
            self.rect.y -= int(PIXELS_PER_SECOND * dt)
            self.direction = "up"
            self.is_moving = True
            
            # Check for y-axis collisions
            if level and (level.check_wall_collision(self) or level.check_fence_collision(self)):
                self.rect.y = self.y

        elif keys[pygame.K_DOWN]:
            self.y = self.rect.y
            self.rect.y += int(PIXELS_PER_SECOND * dt)
            self.direction = "down"
            self.is_moving = True
            
            # Check for y-axis collisions
            if level and (level.check_wall_collision(self) or level.check_fence_collision(self)):
                self.rect.y = self.y

        if self.walk_sound:
            if self.is_moving and not self.walk_sound_playing:
                self.walk_sound.play(-1)
                self.walk_sound_playing = True
            elif not self.is_moving and self.walk_sound_playing:
                self.walk_sound.stop()
                self.walk_sound_playing = False

        self.x = self.rect.x
        self.y = self.rect.y

        super().update(dt, level)

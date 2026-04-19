import pygame

from src.settings import DUCK_SPRITESHEET_ABS_PATH, COW_SPRITESHEET_ABS_PATH
from src.sprites.game_sprite import GameSprite

class Duck(GameSprite):
    
    def __init__(self, x, y, scale):
        """
        Goes through the frames of the duck sprite sheet given its dimensions and saves
        the images of each frame to the frame arrays for the cow sprite instance
        """

        super().__init__(scale)

        self.spriteID = 1
        self.sound_playing = False

        # Set sprite sheet image
        try:
            self.sprite_sheet = pygame.image.load(DUCK_SPRITESHEET_ABS_PATH)
        except FileNotFoundError:
            print("Error: Could not find 'assets/images/sprites/duck_spritesheet.png'")
            return
        
        try:
            self.sound = pygame.mixer.Sound("assets/images/sfx/flap.mp3")
            self.sound.set_volume(0.5)
        except FileNotFoundError:
            print("Error: Could not find flap sound")
            self.sound = None

        self.standing_img = self.get_image(x=0, y=0, width=16, height=20, scale=scale)


        for i in range(4):      #FIXME: Update the x and y values for sprite sheet dimensions
            # Row 1 (Right): X moves by [   ] pixels each loop
            self.walk_right_frames.append(self.get_image(x=i * 16, y=21, width=16, height=20, scale=scale, flip_x=True))

            # Row 1 (Left): Same as above, but flipped
            self.walk_left_frames.append(
                self.get_image(x=i * 16, y=21, width=16, height=20, scale=scale))

            # Row 2 (Down): X moves by [   ] pixels each loop
            self.walk_down_frames.append(self.get_image(x=i * 18, y=40, width=18, height=19, scale=scale))

            # Row 3 (Up): X moves by [   ] pixels each loop
            self.walk_up_frames.append(self.get_image(x=i * 18, y=59, width=18, height=19, scale=scale))

        # Set a starting image for the sprite [Default to standing not flying]
        self.image = self.standing_img

        # Set rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, dt=1, level=None):
        """ Handles Player info for animation """

        PIXELS_PER_SECOND = 225

        # Get the keys that are currently being pressed
        keys = pygame.key.get_pressed()

        # Reset movement for movement check
        self.is_moving = False

        # Determine Movement Direction 
        # [ Duck movement controlled by WASD ]
        if keys[pygame.K_a]:
            self.rect.x -= int(PIXELS_PER_SECOND * dt)
            self.direction = "left"
            self.is_moving = True

        elif keys[pygame.K_d]:
            self.rect.x += int(PIXELS_PER_SECOND * dt)
            self.direction = "right"
            self.is_moving = True

        elif keys[pygame.K_w]:
            self.rect.y -= int(PIXELS_PER_SECOND * dt)
            self.direction = "up"
            self.is_moving = True

        elif keys[pygame.K_s]:
            self.rect.y += int(PIXELS_PER_SECOND * dt)
            self.direction = "down"
            self.is_moving = True

        # Set Boundaries so the duck can't leave the screen
        screen_bounds = pygame.Rect(0, 0, 1280, 720)
        self.rect.clamp_ip(screen_bounds)

        if self.sound:
            if self.is_moving and not self.sound_playing:
                self.sound.play(-1)
                self.sound_playing = True
            elif not self.is_moving and self.sound_playing:
                self.sound.stop()
                self.sound_playing = False

        self.x = self.rect.x
        self.y = self.rect.y

        super().update(dt)
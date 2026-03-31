import pygame

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, scale: int):

        super().__init__()

        self.scale = scale
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.walk_down_frames = []
        self.walk_up_frames = []

        # Animation Variables
        self.frame_index = 0.0
        self.animation_speed = 0.15
        self.direction = "right"
        self.speed = 4
        self.is_moving = False


    def get_image(self, x, y, width, height, scale, colour=None, flip_x=False):
        """   Creates a pygame surface, then goes into the sprite sheet and extracts an image for a given frame   """

        # Create a blank surface
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill((0, 0, 0, 0))        # Fill the surface with transparent pixels

        # Put the cut image extracted from the sheet onto the surface
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        # Scale the image
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # Flip the image if moving Right to Left
        if flip_x:
            image = pygame.transform.flip(image, True, False)

        # Deal with background color
        if colour is not None:
            image.set_colorkey(colour)

        return image

    def update(self, dt=1):
        """ Handles animation """

        if self.is_moving:

            # Increase the frame index by the animation speed
            self.frame_index += self.animation_speed * 60 *dt

            # Each row has four frames, so loop back around after fourth frame
            if self.frame_index >= 4:
                self.frame_index = 0

            # Pick which list of frames to use based on the direction
            match self.direction:
                case "left":
                    frame_list = self.walk_left_frames

                case "right":
                    frame_list = self.walk_right_frames

                case "up":
                    frame_list = self.walk_up_frames

                case "down":
                    frame_list = self.walk_down_frames

            # Update self.image with the new image
            self.image = frame_list[int(self.frame_index)]

        else:
            # If not moving, set the animation to a frame that's standing still
            self.frame_index = 0

            match self.direction:
                case "left":
                    self.image = self.walk_left_frames[0]

                case "right":
                    self.image = self.walk_right_frames[0]

                case "up":
                    self.image = self.walk_up_frames[0]

                case "down":
                    self.image = self.walk_down_frames[0]

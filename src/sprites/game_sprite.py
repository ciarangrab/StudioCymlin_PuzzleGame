import pygame
from src.settings import LEVEL_1_COLL_MASK

class GameSprite(pygame.sprite.Sprite):

    type_of_sprite = {0: "cow", 1: "duck", 2: "object"}

    def __init__(self, scale: int):

        super().__init__()

        self.scale = scale
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.walk_down_frames = []
        self.walk_up_frames = [] 
        self.spriteID = -1
        self.standing_img = None

        # Holds temp position during movement
        self.x = 0
        self.y = 0

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

    def update(self, dt=1, level=None):
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

            # Update the self.rect to match the new image
            self.rect = self.image.get_rect()

            # Update the new rect with the updated position
            self.rect.topleft = (self.x, self.y)

        else:
            # If not moving, set the animation to a frame that's standing still

            match (self.spriteID):
                # For the cow, the still frame to stop on should be based on movement direction
                case 0:
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

                # For the duck, the duck should stop flying and stand still, which is the same image regardless of direction
                case 1:
                    self.image = self.standing_img

        self.mask = pygame.mask.from_surface(self.image)
import pygame
import os


class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=2):
        super().__init__()
        
        spritesheet_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                'assets',
                'images',
                'sprites',
                'objects',
                'Bars_1.png'
            )
        )
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        
        # Fence dimensions: width=50, height=30
        frame_width = 44
        frame_height = 30
        frame_count = self.spritesheet.get_width() // frame_width
        
        # Extract all frames
        self.frames = []
        for i in range(frame_count):
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)
        
        # Animation setup
        self.frame_index = len(self.frames) - 1
        self.animation_speed = 8  # frames per second
        self.frame_timer = 0
        self.animating = False
        self.animation_direction = -1  # 1 for forward, -1 for backward
        
        self.image = self.frames[-1]
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def animate(self, dt):
        if self.animating:
            # Track time until next frame
            self.frame_timer += dt
            frame_duration = 1.0 / self.animation_speed  # Time per frame
            
            if self.frame_timer >= frame_duration:
                self.frame_timer = 0
                self.frame_index += self.animation_direction
                
                # Check bounds and stop animation
                if self.animation_direction == 1:  # Forward
                    if self.frame_index >= len(self.frames) - 1:
                        self.frame_index = len(self.frames) - 1
                        self.animating = False
                else:  # Backward
                    if self.frame_index <= 0:
                        self.frame_index = 0
                        self.animating = False
            
            self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)

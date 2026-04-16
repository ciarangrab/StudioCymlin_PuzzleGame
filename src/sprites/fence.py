import pygame
import os
from src.settings import FENCE_1_ABS_PATH, FENCE_2_ABS_PATH, FENCE_3_ABS_PATH, FENCE_5_ABS_PATH, FENCE_6_ABS_PATH

class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y, fence_type=0, scale=2):
        super().__init__()

        fences = {0:FENCE_1_ABS_PATH, 1: FENCE_2_ABS_PATH, 2: FENCE_3_ABS_PATH, 3: FENCE_5_ABS_PATH, 4: FENCE_6_ABS_PATH}
        
        match (fence_type):
            case 0:
                spritesheet_path = fences.get(fence_type)
                frame_width = 64
                frame_height = 30
            case 1:
                spritesheet_path = fences.get(fence_type)
                frame_width = 8 
                frame_height = 81
            case 2:
                spritesheet_path = fences.get(fence_type)
                frame_width = 44 
                frame_height = 30
            case 3:
                spritesheet_path = fences.get(fence_type)
                frame_width = 54 
                frame_height = 30
            case 4:
                spritesheet_path = fences.get(fence_type)
                frame_width = 8 
                frame_height = 81

        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        
        # Fence dimensions: width=50, height=30
        frame_count = self.spritesheet.get_width() // frame_width
        
        # Extract all frames
        self.frames = []
        for i in range(frame_count):
            frame = self.spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            self.frames.append(frame)
        
        # Create transparent image for when fence is fully down
        self.transparent_surface = pygame.Surface((frame_width * scale, frame_height * scale), pygame.SRCALPHA)
        
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
        
        # Fence is visible at all times EXCEPT when fully down (frame 0)
        if self.frame_index == 0:
            # Use transparent image when fully down
            self.image = self.transparent_surface
        else:
            # Use normal frame image when not at frame 0
            self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt, level=None):
        self.animate(dt)

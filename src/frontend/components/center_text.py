import pygame as pg
from src.frontend.animation.float_animation import FloatAnimation
from src.frontend.animation.scale_animation import ScaleAnimation
from src.frontend.animation.rotate_animation import RotateAnimation
from src import data

class CenterText:
    min_rotate_angle = -3
    max_rotate_angle = 3

    min_scale = 100
    max_scale = 120

    def __init__(self, text: str, font: pg.font.Font, color: pg.Color, center: tuple, fade_in_time=0.5, fade_out_time=0.5):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.center = center
        self.fade_in_time = fade_in_time
        self.fade_out_time = fade_out_time
        self.state = 'scale_in'  # 'scale_in', 'steady', 'scale_out', 'done'

        # Render text once
        self.original_surface = font.render(self.text, True, self.color).convert_alpha()
        self.original_rect = self.original_surface.get_rect(center=center)

        self.surface = self.original_surface.copy()
        self.rect = self.original_rect.copy()

        # Animations
        self.shake = FloatAnimation()

        self.active_scale_animation = ScaleAnimation(self.rect, start_scale=0, end_scale=self.min_scale, duration=fade_in_time)
        self.scaling_down = True
        self.scale_up = ScaleAnimation(self.rect.copy(), start_scale=self.min_scale, end_scale=self.max_scale)
        self.scale_down = ScaleAnimation(self.rect.copy(), start_scale=self.max_scale, end_scale=self.min_scale)

        self.active_rotate_animation = RotateAnimation(self.rect, self.min_rotate_angle, duration=fade_in_time)
        self.rotating_right = False
        self.rotate_left = RotateAnimation(self.rect.copy(), start_angle=self.max_rotate_angle, end_angle=self.min_rotate_angle)
        self.rotate_right = RotateAnimation(self.rect.copy(), start_angle=self.min_rotate_angle, end_angle=self.max_rotate_angle)

        self.busy = True
        self.waiting_to_scale_out = False

    def is_done(self):
        return not self.busy

    def stop(self):
        if self.state != 'scale_out':
            self.state  = 'scale_out'
            current_scale = self.active_scale_animation.get_current_scale()
            self.active_scale_animation = ScaleAnimation(self.rect.copy(), start_scale=current_scale * 100, end_scale=0, duration=self.fade_out_time)

    def draw(self) -> tuple:
        if self.state == 'done':
            self.busy = False
            return

        # Start with a fresh copy
        working_surface = self.original_surface.copy()
        working_rect = self.original_rect.copy()

        # Apply current animations
        working_surface, working_rect = self.active_scale_animation.animate(working_surface, working_rect)
        working_surface, working_rect = self.active_rotate_animation.animate(working_surface, working_rect)
        working_surface, working_rect = self.shake.animate(working_surface, working_rect)

        # Handle state changes
        if self.state == 'scale_in':
            if self.active_scale_animation.is_done():
                self.state = 'steady'
                self.active_scale_animation = self.scale_up
                self.scaling_down = False
                self.active_rotate_animation = self.rotate_right
                self.rotating_right = True
                self.active_scale_animation.reset()
                self.active_rotate_animation.reset()

        elif self.state == 'steady':
            # if self.waiting_to_scale_out and self.active_scale_animation.is_done():
            #     # Start scale-out to 0 from current scale
            #     current_scale = self.active_scale_animation.get_current_scale()
            #     self.active_scale_animation = ScaleAnimation(self.rect.copy(), start_scale=current_scale * 100, end_scale=0, duration=self.fade_out_time)
            #     self.state = 'scale_out'

            if self.active_scale_animation.is_done():
                if self.scaling_down:
                    self.active_scale_animation = self.scale_up
                    self.scaling_down = False
                else:
                    self.active_scale_animation = self.scale_down
                    self.scaling_down = True
                self.active_scale_animation.reset()

            if self.active_rotate_animation.is_done():
                if self.rotating_right:
                    self.active_rotate_animation = self.rotate_left
                    self.rotating_right = False
                else:
                    self.active_rotate_animation = self.rotate_right
                    self.rotating_right = True
                self.active_rotate_animation.reset()

        elif self.state == 'scale_out':
            if self.active_scale_animation.is_done():
                self.state = 'done'

        data.APP_SURFACE.blit(working_surface, working_rect)

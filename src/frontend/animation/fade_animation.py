import pygame as pg
from src.frontend.animation.animation import Animation

class FadeAnimation(Animation):
    def __init__(self, surface: pg.Surface, duration: float = 1.0, mode: str = "in", easing: str = "linear", alpha_bounds: tuple[int, int] = (0, 255)):
        """
        mode: "in", "out", "in-out"
        easing: "linear", "ease-in", "ease-out", "ease-in-out"
        """
        super().__init__()
        self.original_surface = surface.convert_alpha()
        self.duration = duration
        self.mode = mode
        self.easing = easing
        self.start_time = pg.time.get_ticks()
        self.busy = True
        
        if len(alpha_bounds) == 2:   
            self.alpha_bounds = (max(0, min(alpha_bounds)), min(255, max(alpha_bounds)))
        else:
            self.alpha_bounds = (0, 255)

    def _apply_easing(self, t: float) -> float:
        if self.easing == "ease-in":
            return t * t
        elif self.easing == "ease-out":
            return 1 - (1 - t) * (1 - t)
        elif self.easing == "ease-in-out":
            return 2*t*t if t < 0.5 else 1 - pow(-2*t + 2, 2) / 2
        return t  # linear

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed = (current_time - self.start_time) / 1000
        t = min(elapsed / self.duration, 1.0)
        eased_t = self._apply_easing(t)

        if self.mode == "in":
            alpha = int(self.alpha_bounds[1] * eased_t)
        elif self.mode == "out":
            alpha = int(self.alpha_bounds[1] * (1 - eased_t))
        elif self.mode == "in-out":
            if eased_t < 0.5:
                alpha = int(self.alpha_bounds[1] * (eased_t * 2))
            else:
                alpha = int(self.alpha_bounds[1] * (1 - ((eased_t - 0.5) * 2)))
        else:
            alpha = self.alpha_bounds[1]

        alpha = max(self.alpha_bounds[0], min(self.alpha_bounds[1], alpha))

        faded_surface = self.original_surface.copy()
        faded_surface.set_alpha(alpha)

        if t >= 1.0:
            self.busy = False

        return faded_surface, rect

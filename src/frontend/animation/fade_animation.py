import pygame as pg
from src.frontend.animation.animation import Animation

class FadeAnimation(Animation):
    def __init__(self, surface: pg.Surface, duration: float = 1.0, mode: str = "in", easing: str = "linear"):
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
            alpha = int(255 * eased_t)
        elif self.mode == "out":
            alpha = int(255 * (1 - eased_t))
        elif self.mode == "in-out":
            if eased_t < 0.5:
                alpha = int(255 * (eased_t * 2))
            else:
                alpha = int(255 * (1 - ((eased_t - 0.5) * 2)))
        else:
            alpha = 255

        alpha = max(0, min(255, alpha))

        faded_surface = self.original_surface.copy()
        faded_surface.set_alpha(alpha)

        if t >= 1.0:
            self.busy = False

        return faded_surface, rect

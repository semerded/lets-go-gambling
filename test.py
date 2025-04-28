import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a simple card surface
card_front = pygame.Surface((100, 150))
card_front.fill((255, 0, 0))  # Red card

card_back = pygame.Surface((100, 150))
card_back.fill((0, 0, 255))  # Blue card

class Card:
    def __init__(self, front, back, pos):
        self.front_surface = front
        self.back_surface = back
        self.showing_front = True
        self.current_surface = self.front_surface
        self.pos = pos
        self.width = front.get_width()
        self.height = front.get_height()
        self.angle = 0
        self.flipping = False
        self.flip_progress = 0.0  # 0 to 1

    def start_flip(self):
        if not self.flipping:
            self.flipping = True
            self.flip_progress = 0.0

    def update(self):
        if self.flipping:
            self.flip_progress += 0.05  # Flip speed
            if self.flip_progress >= 1.0:
                self.flip_progress = 1.0
                self.flipping = False

            # Switch front/back at halfway
            if self.flip_progress > 0.5 and self.showing_front:
                self.showing_front = False
                self.current_surface = self.back_surface

            # Angle: 0 -> 90 -> 0 (flip effect)
            if self.flip_progress <= 0.5:
                self.angle = 180 * self.flip_progress
            else:
                self.angle = 180 * (1 - self.flip_progress)

    def draw(self, surface):
        # Rotate the current surface
        scaled_surface = pygame.transform.scale(
            self.current_surface,
            (max(1, int(self.width * math.cos(math.pi * self.flip_progress))), self.height)
        )
        rotated_surface = pygame.transform.rotate(scaled_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.pos[0] + self.width // 2, self.pos[1] + self.height // 2))
        surface.blit(rotated_surface, rotated_rect.topleft)

card = Card(card_front, card_back, (350, 225))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                card.start_flip()

    card.update()

    screen.fill((30, 30, 30))
    card.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

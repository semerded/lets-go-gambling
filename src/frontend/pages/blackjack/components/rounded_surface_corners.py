import pygame

def round_corners(surface, radius):
    width, height = surface.get_size()

    # Create a fully transparent surface
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))

    # Draw opaque rounded rectangle (white color with full alpha)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, width, height), border_radius=radius)

    # Copy original surface onto a new one with SRCALPHA
    rounded_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rounded_surface.blit(surface, (0, 0))
    
    # Apply mask
    rounded_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return rounded_surface
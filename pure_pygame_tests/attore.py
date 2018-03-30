import pygame


class Attore:

    def __init__(self, immagine):
        self.immagine = pygame.image.load(immagine).convert_alpha()
        self.x = 0
        self.y = 0
    
    def disegna(self, schermo):
        schermo.blit(self.immagine, [self.x, self.y])

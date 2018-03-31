import pygame


# Classe generica per gli attori protagonisti del gioco
class Attore:

    # Inizializzazione
    def __init__(self, immagine):

        # Carico come immagine il file al percorso passato come parametro
        self.immagine = pygame.image.load(immagine).convert_alpha()

        # Attributi per gestire la posizione dell'attore
        self.x = 0
        self.y = 0

    # Metodo per stampare la propria immagine su una superficie
    def disegna(self, superficie):
        superficie.blit(self.immagine, [self.x, self.y])

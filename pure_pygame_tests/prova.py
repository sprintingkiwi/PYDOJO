import pygame
import attore

print("Ciao Pygame")

schermo = pygame.display.set_mode([1280, 720])

pippo = attore.Attore("pesce.png")

while True:
    for event in pygame.event.get():
        print(event)

    pippo.disegna(schermo)
    
    pygame.display.update()
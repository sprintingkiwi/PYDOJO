import pygame
import attore
import pesce

print("Ciao Pygame")

schermo = pygame.display.set_mode([1280, 720])
orologio = pygame.time.Clock()

pippo = pesce.Pesce("pesce.png")

while True:
    for event in pygame.event.get():
        print(event)

    schermo.fill([20, 20, 50])
    pippo.disegna(schermo)
    pippo.x += 1

    orologio.tick(60)
    pygame.display.update()

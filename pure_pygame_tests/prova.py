import pygame
import attore
import pesce

print("Ciao Pygame")

# Creo lo schermo di gioco
schermo = pygame.display.set_mode([1280, 720])

# Creo un oggetto orologio per gestire il tempo
orologio = pygame.time.Clock()

# Istanzio un personaggio
pippo = pesce.Pesce("immagini/pesce.png")

while True:

    # Scorro la lista degli eventi
    for event in pygame.event.get():

        print(event)

        #  Se clicco la X si chiude il gioco
        if event.type == pygame.QUIT:
            quit()

    # Sposto il mio personaggio
    pippo.x += 1

    # Riempo lo sfondo dello schermo
    schermo.fill([20, 20, 50])
    # Disegno il mio personaggio
    pippo.disegna(schermo)

    # Attendo il tempo necessario per rimanere a 60 fps
    orologio.tick(60)

    #  Aggiorno lo schermo
    pygame.display.update()

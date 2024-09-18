import pygame

# Initialisiere Pygame
pygame.init()
pygame.mixer.init()  # Soundmixer für Musik und Soundeffekte

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Bildschirmgröße festlegen
SCREEN_WIDTH = 600  # Breiter als das Spielfeld, damit Platz für die Benutzeroberfläche bleibt
SCREEN_HEIGHT = 600

# Blockgröße für die Tetris-Steine
BLOCK_SIZE = 30

# Spielfeldgröße in Blöcken (10 Blöcke breit, 20 Blöcke hoch)
FIELD_WIDTH = 10
FIELD_HEIGHT = 20

# Spielgeschwindigkeit (Bildwiederholrate)
FPS = 120

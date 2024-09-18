import pygame
import random

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

# Musik laden und abspielen
pygame.mixer.music.load('Tetris.mp3')  # Lade die Musikdatei
# pygame.mixer.music.play(-1)  # Spiele die Musik in Endlosschleife

# Definiere die Tetris-Formen und ihre Rotationen
SHAPES = [
    [['.....',
      '..O..',
      '..O..',
      '..O..',
      '..O..'],
     ['.....',
      '.....',
      '.....',
      'OOOO.',
      '.....']],
    [['..OO.',
      '..O..',
      '..O..',
      '.....',
      '.....'],
     ['.OOO.',
      '...O.',
      '.....',
      '.....',
      '.....'],
     ['...O.',
      '...O.',
      '..OO.',
      '.....',
      '.....'],
     ['.O...',
      '.OOO.',
      '.....',
      '.....',
      '.....']],
    [['...O.',
      '.OOO.',
      '.....',
      '.....',
      '.....'],
     ['.O...',
      '.O...',
      '.OO..',
      '.....',
      '.....'],
     ['.OOO.',
      '.O...',
      '.....',
      '.....',
      '.....'],
     ['..OO.',
      '...O.',
      '...O.',
      '.....',
      '.....']],
    [['..OO.',
      '..OO.',
      '.....',
      '.....',
      '.....']],
    [['..OO.',
      '.OO..',
      '.....',
      '.....',
      '.....'],
     ['.O...',
      '.OO..',
      '..O..',
      '.....',
      '.....']],
    [['.OO..',
      '..OO.',
      '.....',
      '.....',
      '.....'],
     ['...O.',
      '..OO.',
      '..O..',
      '.....',
      '.....']],
    [['.OOO.',
      '..O..',
      '.....',
      '.....',
      '.....'],
     ['..O..',
      '.OO..',
      '..O..',
      '.....',
      '.....'],
     ['..O..',
      '.OOO.',
      '.....',
      '.....',
      '.....'],
     ['..O..',
      '..OO.',
      '..O..',
      '.....',
      '.....']]
]

# Farben für die Formen, die den SHAPES zugeordnet werden
SHAPE_COLORS = [
    (0, 255, 255),
    (0, 0, 255),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128)
]

# Klasse für die einzelnen Tetris-Steine
class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # x-Position auf dem Spielfeld
        self.y = y  # y-Position auf dem Spielfeld
        self.shape = shape  # Die Form des Steins
        self.color = SHAPE_COLORS[SHAPES.index(shape)]  # Die Farbe des Steins basierend auf seiner Form
        self.rotation = 0  # Rotationsstatus des Steins

# Erstelle ein Gitter, das das Spielfeld darstellt
def create_grid(locked_positions={}):
    # Ein zweidimensionales Array, das das Spielfeld in Schwarz darstellt
    grid = [[BLACK for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]

    # Füge die gesperrten (platzierten) Positionen in das Gitter ein
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            if (x, y) in locked_positions:  # Überprüfe, ob an dieser Position ein Block gesperrt ist
                color = locked_positions[(x, y)]  # Farbe des gesperrten Blocks
                grid[y][x] = color  # Setze die Blockfarbe im Gitter

    return grid  # Gib das Gitter zurück

# Konvertiere die aktuelle Form in Positionen auf dem Spielfeld
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]  # Rotationsstatus der Form

    # Gehe durch jede Zeile und Spalte der Form
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':  # Wenn 'O' gefunden wird, ist dies ein Teil des Blocks
                positions.append((piece.x + j, piece.y + i))  # Speichere die Position relativ zur Spielfeldkoordinate

    # Korrigiere die Positionen basierend auf der Anzeige im Gitter
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# Überprüfe, ob ein Block an einer gültigen Position ist (nicht in anderen Blöcken oder außerhalb des Spielfelds)
def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(FIELD_WIDTH) if grid[y][x] == BLACK] for y in range(FIELD_HEIGHT)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted = convert_shape_format(piece)

    # Überprüfe, ob die aktuelle Form gültig ist
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Überprüfe, ob das Spiel verloren ist (wenn ein Block die oberste Reihe erreicht)
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Wähle zufällig eine neue Form aus
def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

# Zeichne den Text in der Mitte des Bildschirms
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    label = font.render(text, 1, color)

    # Platziere den Text in der Mitte des Bildschirms
    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2, SCREEN_HEIGHT / 2 - label.get_height() / 2))

# Zeichne das Gitter und die darin enthaltenen Blöcke
def draw_grid(surface, grid):
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # Zeichne die Linien des Gitters
    draw_grid_lines(surface)

# Zeichne die Gitterlinien
def draw_grid_lines(surface):
    for y in range(FIELD_HEIGHT):
        pygame.draw.line(surface, WHITE, (0, y * BLOCK_SIZE), (FIELD_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
    for x in range(FIELD_WIDTH):
        pygame.draw.line(surface, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, FIELD_HEIGHT * BLOCK_SIZE))

# Überprüfe und entferne vollständige Reihen
def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if BLACK not in row:  # Wenn keine schwarzen Blöcke vorhanden sind, ist die Reihe voll
            increment += 1
            ind = y
            for x in range(len(row)):
                try:
                    del locked[(x, y)]  # Entferne die gesperrten Blöcke in dieser Reihe
                except:
                    continue

    # Verschiebe alle oberen Reihen nach unten
    if increment > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment

# Zeichne die nächste Form, die erscheinen wird
def draw_next_shape(shape, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = FIELD_WIDTH * BLOCK_SIZE + 50
    sy = SCREEN_HEIGHT / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    # Zeichne die nächste Form in einem kleinen Vorschaufenster
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

# Zeichne den aktuellen Punktestand auf den Bildschirm
def draw_score(surface, score):
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render(f'Score: {score}', 1, WHITE)

    sx = FIELD_WIDTH * BLOCK_SIZE + 50
    sy = SCREEN_HEIGHT / 2 - 200
    surface.blit(label, (sx + 10, sy))

# Hauptspielfunktion
def main():
    locked_positions = {}  # Gesperrte Positionen (bereits platzierte Blöcke)
    grid = create_grid(locked_positions)  # Erstelle das Spielfeld
    print (grid)

    # Setze die Hintergrundmusik bei Spielbeginn fort
    pygame.mixer.music.play(-1)  # Spiele die Musik in Endlosschleife
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')  # Setze den Fenstertitel

    change_piece = False  # Gibt an, ob die aktuelle Form fallen gelassen wurde
    run = True  # Spiel läuft
    current_piece = get_shape()  # Aktuelle Form
    next_piece = get_shape()  # Nächste Form
    clock = pygame.time.Clock()  # Spieluhr
    fall_time = 0  # Zeit, bis die Form fällt
    points = 0  # Punktestand

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        grid = create_grid(locked_positions)  # Aktualisiere das Spielfeld
        fall_speed = 0.27  # Fallgeschwindigkeit

        fall_time += clock.get_rawtime()
        clock.tick()

        # Überprüfe, ob genug Zeit vergangen ist, damit die Form fallen kann
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Überprüfe Benutzerereignisse (Tastendrücke)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # Bewege die Form nach links
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1  # Rückgängig, wenn ungültig
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # Bewege die Form nach rechts
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1  # Bewege die Form nach unten
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)  # Drehe die Form
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)  # Konvertiere die aktuelle Form in Spielfeldpositionen

        # Zeichne die aktuelle Form in das Gitter
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Wenn die Form fallen gelassen wurde, sperre sie
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece  # Setze die nächste Form als aktuelle Form
            next_piece = get_shape()  # Wähle eine neue Form als nächste
            change_piece = False

            cleared_rows = clear_rows(grid, locked_positions)  # Überprüfe und lösche volle Reihen
            if cleared_rows:
                points += cleared_rows * 100  # 100 Punkte pro gelöschter Reihe

        screen.fill(BLACK)  # Fülle den Hintergrund schwarz
        pygame.draw.rect(screen, GRAY, (0, 0, FIELD_WIDTH * BLOCK_SIZE, FIELD_HEIGHT * BLOCK_SIZE), 5)  # Rahmen um das Spielfeld

        draw_grid(screen, grid)  # Zeichne das Spielfeld
        draw_next_shape(next_piece, screen)  # Zeichne die nächste Form
        draw_score(screen, points)  # Zeige den Punktestand an
        pygame.display.update()  # Aktualisiere den Bildschirm

        # Überprüfe, ob das Spiel verloren wurde
        if check_lost(locked_positions):
            screen.fill(BLACK)
            draw_text_middle("YOU LOST", 80, WHITE, screen)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False  # Beende das Spiel

# Hauptmenü-Funktion, die das Spiel startet
def main_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    run = True  # Menü läuft
    while run:
        screen.fill(GRAY)
        draw_text_middle('Press to Play', 60, WHITE, screen)
        pygame.display.update()

        # Überprüfe Benutzerereignisse im Menü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Beende das Menü
            if event.type == pygame.KEYDOWN:
                main()  # Starte das Spiel, wenn eine Taste gedrückt wird

    pygame.quit()  # Beende das Spiel und schließe das Fenster


main_menu()

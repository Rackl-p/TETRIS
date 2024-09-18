from shapes import SHAPES, SHAPE_COLORS

class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # x-Position auf dem Spielfeld
        self.y = y  # y-Position auf dem Spielfeld
        self.shape = shape  # Die Form des Steins
        self.color = SHAPE_COLORS[SHAPES.index(shape)]  # Die Farbe des Steins basierend auf seiner Form
        self.rotation = 0  # Rotationsstatus des Steins

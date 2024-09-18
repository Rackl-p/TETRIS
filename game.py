import pygame
import random
from constants import *
from piece import Piece
from shapes import SHAPES

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'O':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(FIELD_WIDTH) if grid[y][x] == BLACK] for y in range(FIELD_HEIGHT)]
    accepted_positions = [x for item in accepted_positions for x in item]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            increment += 1
            ind = y
            for x in range(len(row)):
                del locked[(x, y)]
    if increment > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

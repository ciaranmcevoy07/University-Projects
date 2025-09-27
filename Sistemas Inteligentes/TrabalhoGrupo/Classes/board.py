import pygame
from constants import *


def drawGrid(win):
    blockSize = SQUARE_SIZE
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(win, GRID_COLOUR, rect, 1)


def adapt(row, col):
    new_row = row * SQUARE_SIZE
    new_col = col * SQUARE_SIZE
    return new_row, new_col


class Board:
    def __init__(self, max_rows, max_cols):
        self.matrix = []
        self.teams = {}
        self.create_board(max_rows, max_cols)

    def create_board(self, max_rows, max_cols):
        for row in range(max_rows):
            self.matrix.append([])
            for col in range(max_cols):
                self.matrix[row].append(None)

    def draw(self, win):
        blockSize = SQUARE_SIZE - 1
        drawGrid(win)
        for row in range(Y_MAX):
            for col in range(X_MAX):
                colup = Y_MAX - 1 - col
                piece = self.matrix[colup][row]
                if piece is None:
                    x, y = adapt(row, col)
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(win, BACK_COLOUR, rect, blockSize)
                if piece is not None:
                    x, y = adapt(row, col)
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(win, TEAMS[self.teams[piece.getTeam()]], rect, blockSize)

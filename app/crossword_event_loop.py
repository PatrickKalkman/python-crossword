import time
import pygame
from pygame.locals import QUIT

from app.variable import Variable

CELL_SIZE = 120
LINE_WIDTH = 1


class CrosswordEventLoop:
    def __init__(self, crossword):
        pygame.init()
        self.crossword = crossword
        self.screen = pygame.display.set_mode((self.crossword.width*CELL_SIZE,
                                               self.crossword.height*CELL_SIZE))
        pygame.display.set_caption("Crossword")
        pygame.display.update()
        self.assignment = None

    def draw_assignment(self):
        self.screen.fill((0, 0, 0))  # black background
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:  # if the cell can be written to
                    pygame.draw.rect(self.screen, (255, 255, 255), ((j*CELL_SIZE) + LINE_WIDTH, (i*CELL_SIZE) + LINE_WIDTH, CELL_SIZE - 2*LINE_WIDTH, CELL_SIZE - 2*LINE_WIDTH))  # white cell
                else:  # if the cell can't be written to
                    pygame.draw.rect(self.screen, (0, 0, 0), (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))  # black cell

        if self.assignment is None:
            return

        assignment_copy = self.assignment.copy()

        for variable, word in assignment_copy.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                if self.crossword.structure[i][j]:
                    # draw text for the letter
                    font = pygame.font.Font(None, 48)
                    text = font.render(word[k], True, (0, 0, 0))  # black text
                    self.screen.blit(text, (j*CELL_SIZE + (CELL_SIZE - text.get_width()) / 2, i*CELL_SIZE + (CELL_SIZE - text.get_height()) / 2))  # center text in cell

        pygame.display.update()

    def update_assignment(self, assignment):
        self.assignment = assignment

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            if self.assignment:
                self.draw_assignment()
        pygame.quit()

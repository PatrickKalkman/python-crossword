import pygame
from pygame.locals import QUIT

from app.variable import Variable

CELL_SIZE = 120
LINE_WIDTH = 1


class CrosswordEventLoop:
    def __init__(self, crossword):
        self.crossword = crossword
        self.assignment = None
        self.running = True

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.crossword.width * CELL_SIZE,
                                               self.crossword.height * CELL_SIZE))
        pygame.display.set_caption("Crossword")

    def terminate_pygame(self):
        pygame.quit()

    def draw_cell(self, i, j):
        color = (255, 255, 255) if self.crossword.structure[i][j] else (0, 0, 0)
        pygame.draw.rect(self.screen, color,
                         (j * CELL_SIZE,
                          i * CELL_SIZE,
                          CELL_SIZE,
                          CELL_SIZE))

        if self.crossword.structure[i][j]:
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (j * CELL_SIZE,
                              i * CELL_SIZE,
                              CELL_SIZE,
                              CELL_SIZE),
                             LINE_WIDTH)

    def draw_letter(self, i, j, letter):
        font = pygame.font.Font(None, 48)
        text = font.render(letter, True, (0, 0, 0))
        self.screen.blit(text,
                         (j * CELL_SIZE + (CELL_SIZE - text.get_width()) / 2,
                          i * CELL_SIZE + (CELL_SIZE - text.get_height()) / 2))

    def draw_assignment(self):
        self.screen.fill((0, 0, 0))

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                self.draw_cell(i, j)

        if self.assignment is None:
            return

        assignment_copy = self.assignment.copy()
        for variable, word in assignment_copy.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                if self.crossword.structure[i][j]:
                    self.draw_letter(i, j, word[k])

        pygame.display.update()

    def update_assignment(self, assignment):
        self.assignment = assignment
        pygame.time.delay(250)

    def finish(self):
        self.running = False

    def run(self):
        self.initialize_pygame()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            if self.assignment:
                self.draw_assignment()
        self.terminate_pygame()

from app.variable import Variable


class Crossword:
    def __init__(self, structure, width, height, words):
        self.structure = structure
        self.width = width
        self.height = height
        self.words = words
        self.variables = set()
        self.overlaps = dict()
        self.variable_to_number = {}
        self.determine_variables()
        self.determine_overlaps()

    def determine_variables(self):
        for i in range(self.height):
            for j in range(self.width):
                self.check_vertical(i, j)
                self.check_horizontal(i, j)
        self.initialize_variable_to_number()

    def determine_overlaps(self):
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 != v2:
                    self.set_overlap(v1, v2)

    def neighbors(self, var):
        return set(v for v in self.variables if v != var and self.overlaps[v, var])

    def check_vertical(self, i, j):
        if self.structure[i][j] and (i == 0 or not self.structure[i - 1][j]):
            length = self.get_vertical_length(i, j)
            if length > 1:
                self.variables.add(Variable(i=i, j=j, direction=Variable.DOWN,
                                            length=length))

    def get_vertical_length(self, i, j):
        length = 1
        for k in range(i + 1, self.height):
            if self.structure[k][j]:
                length += 1
            else:
                break
        return length

    def check_horizontal(self, i, j):
        if self.structure[i][j] and (j == 0 or not self.structure[i][j - 1]):
            length = self.get_horizontal_length(i, j)
            if length > 1:
                self.variables.add(Variable(i=i, j=j, direction=Variable.ACROSS,
                                            length=length))

    def get_horizontal_length(self, i, j):
        length = 1
        for k in range(j + 1, self.width):
            if self.structure[i][k]:
                length += 1
            else:
                break
        return length



    def set_overlap(self, v1, v2):
        cells1 = v1.cells
        cells2 = v2.cells
        intersection = set(cells1).intersection(cells2)
        if not intersection:
            self.overlaps[v1, v2] = None
        else:
            overlap_point = intersection.pop()
            self.overlaps[v1, v2] = (cells1.index(overlap_point),
                                     cells2.index(overlap_point))

    def get_variable_at_cell(self, i, j):
        for variable in self.variables:
            if variable.i == i and variable.j == j:
                return variable
        return None

    def initialize_variable_to_number(self):
        number = 1
        starting_point_to_number = {}
        for variable in sorted(self.variables,
                               key=lambda var: (var.i, var.j, var.direction)):
            starting_point = (variable.i, variable.j)
            if starting_point not in starting_point_to_number:
                starting_point_to_number[starting_point] = number
                number += 1
            self.variable_to_number[variable] = starting_point_to_number[starting_point]

    def _has_across_at(self, i, j):
        for var in self.variables:
            if var.i == i and var.j == j and var.direction == Variable.ACROSS:
                return True
        return False

    def get_variable_number(self, var):
        return self.variable_to_number.get(var, None)

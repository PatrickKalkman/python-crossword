from app.variable import Variable
import pygame


class CrosswordCreator():

    def __init__(self, crossword, callback=None):
        self.callback = callback
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.assignment = None

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var, words in self.domains.items():
            for word in words.copy():
                if len(word) != var.length:
                    words.remove(word)

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revised

        i, j = overlap
        for word_x in self.domains[x].copy():
            # Check if there is a word in y's domain that satisfies the overlap
            if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                self.domains[x].remove(word_x)
                revised = True

        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = [(x, y) for x in self.crossword.variables
                    for y in self.crossword.neighbors(x)]

        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))

        return True

    def assignment_complete(self, assignment):
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        unique = set()
        for var, word in assignment.items():
            if var.length != len(word):
                return False
            if word in unique:
                return False
            unique.add(word)
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if word[i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        heuristics = {}
        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    for word in self.domains[neighbor]:
                        if value[i] != word[j]:
                            count += 1
            heuristics[value] = count
        return sorted(heuristics, key=lambda key: heuristics[key])

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.crossword.variables if v not in assignment]
        return min(unassigned, key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))

    def get_assignment(self):
        return self.assignment

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.callback:
                self.callback(assignment)
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None

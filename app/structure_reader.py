class StructureReader:
    def __init__(self, structure_file):
        self.structure_file = structure_file

    def read_structure(self):
        # Determine structure of crossword
        with open(self.structure_file) as f:
            contents = f.read().splitlines()
            height = len(contents)
            width = max(len(line) for line in contents)

            structure = []
            for i in range(height):
                row = []
                for j in range(width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                structure.append(row)
        return structure, height, width

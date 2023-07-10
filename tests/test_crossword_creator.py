import pytest
from app.crossword import Crossword
from app.variable import Variable
from app.crossword_creator import CrosswordCreator


# Create a fixture for crossword creator
@pytest.fixture
def crossword_creator():
    # Create a simple crossword puzzle
    structure = [
        [True, True, False],
        [True, True, True],
        [False, True, True]
    ]
    words = set(['DOG', 'GOD', 'ODD', 'FISH', 'ADD', 'DAD', 'POPLAR'])
    crossword = Crossword(structure, 3, 3, words)

    # Create the crossword creator
    return CrosswordCreator(crossword)


def test_generate_varables(crossword_creator):
    # Check that the crossword creator has generated the correct number of variables
    assert len(crossword_creator.crossword.variables) == 6

    # Check that the crossword creator has generated the correct variables
    assert Variable(0, 0, 'across', 2) in crossword_creator.crossword.variables
    assert Variable(0, 0, 'down', 2) in crossword_creator.crossword.variables
    assert Variable(0, 1, 'down', 3) in crossword_creator.crossword.variables
    assert Variable(1, 0, 'across', 3) in crossword_creator.crossword.variables
    assert Variable(2, 1, 'across', 2) in crossword_creator.crossword.variables
    assert Variable(1, 2, 'down', 2) in crossword_creator.crossword.variables


def test_enforce_node_consistency(crossword_creator):
    # Check initial state
    for var, words in crossword_creator.domains.items():
        assert len(words) == len(crossword_creator.crossword.words)

    # Enforce node consistency
    crossword_creator.enforce_node_consistency()

    # Check that all words in the domain of each variable are of correct length
    for var, words in crossword_creator.domains.items():
        for word in words:
            assert len(word) == var.length


def test_revise_with_overlap(crossword_creator):
    # Create two variables with initially overlapping domains
    var_x = Variable(0, 0, 'down', 3)
    var_y = Variable(0, 1, 'down', 3)
    crossword_creator.domains[var_x] = set(['DOG', 'GOD', 'ODD'])
    crossword_creator.domains[var_y] = set(['DOG', 'POPLAR', 'DAD'])

    # The overlap is at the second position
    crossword_creator.crossword.overlaps[var_x, var_y] = (1, 0)

    # Check initial state
    assert 'GOD' in crossword_creator.domains[var_x]

    # Revise var_x
    result = crossword_creator.revise(var_x, var_y)

    # Check that 'GOD' has been removed from the domain of var_x,
    # as it does not have an overlap with any word in var_y's domain.
    assert 'GOD' not in crossword_creator.domains[var_x]
    assert result is True


def test_revise_without_overlap(crossword_creator):
    # Create two variables with initially overlapping domains
    var_x = Variable(0, 0, 'down', 3)
    var_y = Variable(0, 1, 'down', 3)
    crossword_creator.domains[var_x] = set(['DOG', 'GOD', 'ODD'])
    crossword_creator.domains[var_y] = set(['DOG', 'POPLAR', 'DAD'])

    # The overlap is at the second position
    crossword_creator.crossword.overlaps[var_x, var_y] = None

    # Revise var_x
    result = crossword_creator.revise(var_x, var_y)

    assert result is False


def test_ac3(crossword_creator):
    # Perform arc consistency
    assert crossword_creator.ac3()

    # Check that no domains are empty
    for var, words in crossword_creator.domains.items():
        assert len(words) > 0

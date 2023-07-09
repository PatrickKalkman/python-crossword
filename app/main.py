import threading
from crossword_answer_generator import CrosswordAnswerGenerator
from structure_reader import StructureReader
from crossword import Crossword
from crossword_creator import CrosswordCreator
from crossword_event_loop import CrosswordEventLoop
from crossword_cue_generator import CrosswordCueGenerator
from pdf_generator import PDFGenerator


def main():
    answer_generator = CrosswordAnswerGenerator()
    short_words = answer_generator.generate(category='nature',
                                            word_length='short',
                                            num_words=200)

    medium_words = answer_generator.generate(category='sports',
                                             word_length='medium',
                                             num_words=200)

    long_words = answer_generator.generate(category='science',
                                           word_length='long',
                                           num_words=200)

    additional_words = answer_generator.get_additional_words()

    all_words = short_words + medium_words + long_words + additional_words

    structure_reader = StructureReader('./structures/structure2.txt')
    structure, height, width = structure_reader.read_structure()
    crossword = Crossword(structure, width, height, all_words)

    event_loop = CrosswordEventLoop(crossword)
    creator = CrosswordCreator(crossword, event_loop.update_assignment, event_loop.finish)
    creator_thread = threading.Thread(target=creator.solve)
    creator_thread.start()
    event_loop.run()
    assignment = creator.assignment
    crossword_cue_generator = CrosswordCueGenerator()
    if assignment is None:
        print("No solution found.")
    else:
        for variable, word in sorted(assignment.items(), key=lambda item: crossword.get_variable_number(item[0])):
            cue = crossword_cue_generator.generate(word)
            print(f"{crossword.get_variable_number(variable)}: {variable.direction} => {cue}")

    pdf_generator = PDFGenerator()
    pdf_generator.create_pdf(assignment, crossword, crossword_cue_generator)


if __name__ == "__main__":
    main()

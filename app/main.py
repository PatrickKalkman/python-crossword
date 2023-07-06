import threading
from crossword_answer_generator import CrosswordAnswerGenerator
from structure_reader import StructureReader
from crossword import Crossword
from crossword_creator import CrosswordCreator
from crossword_event_loop import CrosswordEventLoop


def main():
    answer_generator = CrosswordAnswerGenerator()
    short_words = answer_generator.generate_words(category='nature',
                                                  word_length='short',
                                                  num_words=200)

    medium_words = answer_generator.generate_words(category='sports',
                                                   word_length='medium',
                                                   num_words=200)

    long_words = answer_generator.generate_words(category='science',
                                                 word_length='long',
                                                 num_words=200)

    additional_words = answer_generator.get_additional_words()

    all_words = short_words + medium_words + long_words + additional_words

    structure_reader = StructureReader('./structures/structure0.txt')
    structure, height, width = structure_reader.read_structure()
    crossword = Crossword(structure, width, height, all_words)

    event_loop = CrosswordEventLoop(crossword)
    creator = CrosswordCreator(crossword, event_loop.update_assignment)
    creator_thread = threading.Thread(target=creator.solve)
    creator_thread.start()
    event_loop.run()


if __name__ == "__main__":
    main()

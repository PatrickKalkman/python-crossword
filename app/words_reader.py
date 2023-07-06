class WordsReader:
    def __init__(self, words_file):
        self.words_file = words_file

    def read_words(self):
        # Save vocabulary list
        with open(self.words_file) as f:
            words = set(f.read().upper().splitlines())
        return words

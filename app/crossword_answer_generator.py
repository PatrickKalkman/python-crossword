import os
import json
import openai
from dotenv import load_dotenv


class CrosswordAnswerGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_words(self, category, word_length, num_words):
        cache_file = f"cache/{category}_{word_length}_{num_words}.json"
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                words = json.load(f)
        else:
            prompt = (f"Generate a list of {num_words} {word_length}-syllable"
                      f"English words related to the category '{category}', suitable"
                      "for a crossword puzzle.")

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.9,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )

            print(response)

            words = self._parse_response(response['choices'][0]['text'])
            with open(cache_file, "w") as f:
                json.dump(words, f)

        return words

    def get_additional_words(self):
        with open("cache/additional_words.txt", "r") as f:
            words = f.read().splitlines()
        return [word.lower().strip() for word in words]

    @staticmethod
    def _parse_response(response_text):
        lines = response_text.strip().split('\n')
        words = [line.split(' ', 1)[1] for line in lines if len(line.split(' ', 1)) > 1]
        words = [word.lower().strip() for word in words]
        return words

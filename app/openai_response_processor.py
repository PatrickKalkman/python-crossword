import os
import json
import openai
from dotenv import load_dotenv


class OpenAIResponseProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def _create_prompt(self, *args, **kwargs):
        raise NotImplementedError

    def _parse_response(self, response_text):
        raise NotImplementedError

    def _create_cache_filename(self, category, word_length, num_words):
        raise NotImplementedError

    def generate(self, *args, **kwargs):
        cache_file = self._create_cache_filename(*args, **kwargs)
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                result = json.load(f)
        else:
            prompt = self._create_prompt(*args, **kwargs)

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.9,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )

            result = self._parse_response(response['choices'][0]['text'])  # type: ignore
            with open(cache_file, "w") as f:
                json.dump(result, f)

        return result

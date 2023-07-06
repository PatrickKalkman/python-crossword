from app.openai_response_processor import OpenAIResponseProcessor


class CrosswordCueGenerator(OpenAIResponseProcessor):
    def _create_prompt(self, answer):
        return f"Generate a clue for the crossword answer '{answer}'."

    def _parse_response(self, response_text):
        return response_text.strip()

    def _create_cache_file(self, answer):
        return f"cache/{answer}.json"

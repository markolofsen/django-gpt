import openai
import json


class GPTAssistant:
    def __init__(self, api_key, version: int = 3, language: str = "en", max_length: int = 300, is_html: bool = True, allowed_tags: list = []):
        openai.api_key = api_key
        self.messages = []
        self.version = version
        self.language = language
        self.max_length = max_length
        self.keys = ["request", "body"]

        self.is_html = is_html
        self.allowed_tags = []

        if is_html:
            self.allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                 'ul', 'ol', 'li', 'a', 'br', 'b', 'i', 'strong', 'em', 'u', 'code', 'hr', 'blockquote', 'div']

            if allowed_tags:
                self.allowed_tags = allowed_tags

        self.set_rules()

    def set_rules(self):

        self.add_role('system', f"Your language (iso): {self.language}")

        self.add_role(
            'system', f"Use max_length: {self.max_length} in json.body"
        )

        json_format = json.dumps({key: "str" for key in self.keys})
        self.add_role(
            'system', f"Return response in JSON format with double quotes. Example: {json_format}"
        )

        if self.is_html and self.allowed_tags:
            tags = ", ".join(f"<{tag}>" for tag in self.allowed_tags)
            self.add_role(
                'system', f"In json.body use html tags: {tags}."
            )

    def response_decoder(self, response):
        try:
            for key in self.keys:
                response = response.replace(f"'{key}':", f'"{key}":')

            res = json.loads(response)
            return res["body"]
        except Exception as e:
            print('@' * 30)
            print(f"Error in response_decoder: {e}")
            print(f"Response: {response}")
            # raise Exception(f"Error in response_decoder: {e}")
            return response

    def add_role(self, role, content):
        if isinstance(content, str):
            self.messages.append({"role": role, "content": content})

    def clear_messages(self):
        self.messages = []

    def generate_response(self, temperature: float = 0.7):

        # print(self.messages)

        try:
            model_version = "gpt-3.5-turbo" if self.version == 3 else "gpt-4"
            max_tokens_per_request = 1000  # Max tokens per request

            response_parts = []

            # Split messages into chunks so that each chunk fits within the token limit
            for i in range(0, len(self.messages), max_tokens_per_request):
                chunk_messages = self.messages[i:i + max_tokens_per_request]

                response = openai.ChatCompletion.create(
                    model=model_version,
                    messages=chunk_messages,
                    max_tokens=max_tokens_per_request,
                    temperature=temperature,
                    n=1,
                    stop=None,
                )

                response_content = response.choices[0].message["content"]
                response_parts.append(response_content)

            # Combine all response parts into a single string
            full_response = "".join(response_parts)

            # Clear messages for next request
            self.clear_messages()

            return self.response_decoder(full_response)

        except openai.error.OpenAIError as e:
            raise Exception(f"OpenAI Error: {str(e)}")

    def set_words(self, content: str):
        self.messages.append(
            {"role": "user", "content": content}
        )


if __name__ == "__main__":
    # Set your OpenAI API key
    CHATGPT_API_KEY = "***"

    # Create an instance of the GPTAssistant class
    assistant = GPTAssistant(CHATGPT_API_KEY, language="ru", max_length=300)

    words_to_generate = "Where to buy a house in the city of London?"

    assistant.set_words(words_to_generate)

    assistant.add_role(
        'assistant', "You're a real estate agent and you're writing a description for a property.")

    response = assistant.generate_response()

    print(response)

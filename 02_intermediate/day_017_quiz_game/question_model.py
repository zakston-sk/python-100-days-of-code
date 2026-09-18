class Question:
    """A single quiz question with text and the correct answer."""

    def __init__(self, text: str, answer: str):
        self.text = text
        self.answer = answer

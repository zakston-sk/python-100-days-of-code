class QuizBrain:
    """Handles the quiz logic: asking questions, checking answers, and scoring."""

    def __init__(self, questions: list):
        self.questions = questions
        self.question_index = 0
        self.score = 0

    def still_has_questions(self):
        """Return True if there are more questions to ask."""
        return self.question_index < len(self.questions)

    def next_question(self):
        """Ask the next question and check the user's answer."""
        question = self.questions[self.question_index]
        self.question_index += 1
        user_answer = input(f"Q.{self.question_index}: {question.text} (True/False): ")
        self.check_answer(user_answer, question.answer)

    def check_answer(self, user_answer: str, question_answer: str):
        """Compare the user's answer with the correct one and update the score."""
        if user_answer.lower() == question_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")
        print(f"The correct answer was: {question_answer}.")
        print(f"Your current score is {self.score}/{self.question_index}.\n")
        return user_answer.lower() == question_answer.lower()

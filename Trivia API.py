import requests, random, html
education_id = 9
api_url = f"https://opentdb.com/api.php?amount=10&category={education_id}&type=multiple"
def fetch_trivia_questions():
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0:
            return data['results']
        return None
    
def run_quiz():
    questions = fetch_trivia_questions()
    if not questions:
        print("Failed to retrieve trivia questions.")
        return
    score = 0
    print("Welcome to the Trivia Quiz! Answer the following questions:")
    for i, q in enumerate(questions, 1):
        question = html.unescape(q['question']) #unescape, it converts HTML entities to normal text
        correct = html.unescape(q['correct_answer'])
        incorrect = [html.unescape(ans) for ans in q['incorrect_answers']]
        options = incorrect + [correct]
        random.shuffle(options)
        print(f"\nQ{i}: {question}")
        for idx, options_text in enumerate(options, 1):
            print(f"  {idx}. {options_text}")
        while True:
            try:
                choice = int(input("Your answer (1-4): "))
                if 1 <= choice <= 4:
                    break
            except ValueError:
                pass #invalid input, ask again
            print("Invalid input.", 2)
        if options[choice - 1] == correct:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {correct}")
    print(f"\nQuiz Over! Your final score is {score} out of {len(questions)}.")

if __name__ == "__main__":
    run_quiz()
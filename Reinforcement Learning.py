from hf import generate_response
def reinforcement_learning_activity():
    print("\n=== REINFORCEMENT LEARNING ACTIVITY ===\n")
    prompt = input("Enter a prompt for the AI to respond to: ").strip()
    if not prompt:
        print("No prompt entered. Exiting activity.")
        return

    initial_response = generate_response(prompt)
    print(f"\nAI's initial response: {initial_response}")
    
    try:
        rating = int(input("\nRate the AI's response on a scale of 1-5 (1=poor, 5=excellent): ").strip())
        if rating < 1 or rating > 5:
            print("Invalid rating. Using default rating of 3.")
            rating = 3
    except ValueError:
        print("Invalid input. Using default rating of 3.")
        rating = 3
        
    feedback = input("Provide specific feedback on how the AI's response could be improved: ").strip()
    improved_response = f"{initial_response} (improved based on feedback: {feedback})"
    print(f"\nAI's improved response: {improved_response}")
    print("\n--- Reflection ---")
    print("1. How did your feedback influence the AI's improved response?")
    print("2. How does reinforcement learning help AI to improve over time?")
    
def role_based_prompt():
    print("\n=== ROLE-BASED PROMPT ACTIVITY ===\n")
    category = input("Enter a category (e.g, science, history, art): ").strip()
    item = input("Enter a specific item within that category (e.g, black holes, renaissance art): ").strip()
     
    if not category or not item:
        print("Category and item cannot be empty. Exiting activity.")
        return
    teacher_prompt = f"You are a teacher explaining {item} in the context of {category} to a student."
    expert_prompt = f"You are an expert in {category} providing a detailed explanation of {item}."
    
    teacher_response = generate_response(teacher_prompt, temperature=0.3, max_tokens=1024)
    expert_response = generate_response(expert_prompt, temperature=0.3, max_tokens=1024)
    
    print(f"\nTeacher's response:\n{teacher_response}")
    print(f"\nExpert's response:\n{expert_response}")
    print("\n--- Reflection ---")
    print("1. How did the teacher's response differ from the expert's response?")
    print("2. How can role-based prompting help you get more tailored responses from AI?")
    
def run_activity():
    print("/n=== AI Learning Activities ===\n")
    print("Choose an activity:")
    print("1. Reinforcement Learning Simulation")
    print("2. Role-Based Prompting")
    choice = input(">").strip()
    if choice == "1":
        reinforcement_learning_activity()
    elif choice == "2":
        role_based_prompt()
    else:
        print("Invalid choice. Exiting.")
if __name__ == "__main__":
    run_activity()
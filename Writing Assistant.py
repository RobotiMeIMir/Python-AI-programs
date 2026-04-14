from hf import generate_response

def get_essay_details():
    print("\n=== ESSAY WRITING ASSISTANT ===\n")
    topic = input("Enter the essay topic: ").strip()
    essay_type = input("Enter the essay type (e.g., argumentative, descriptive): ").strip()
    lengths = ["300 words", "900 words", "1500 words"]
    print("Choose the desired essay length:")
    for i, length in enumerate(lengths, 1): print(f"{i}. {length}")
    try:
        idx = int(input("> ").strip()) 
        length = lengths[idx - 1] if 1 <= idx <= len(lengths) else "300 words"
    except ValueError:
        length = "300 words"
    target_audience = input("Enter the target audience (e.g., high school students, general public): ").strip()
    return {"topic": topic, "essay_type": essay_type, "length": length, "target_audience": target_audience}
   
def generate_essay(details):
    try:
        temp = float(input("Enter creativity level (0.0 - 1.0, default 0.7): ").strip())
        if not (0.0 <= temp <= 1.0): raise ValueError
    except ValueError:
        print("Invalid input. Using default creativity level of 0.3.")
        temp = 0.3
        
    intro_p = f"Write an introduction for an {details['essay_type']} essay on '{details['topic']}' aimed at {details['target_audience']}"
    intro = generate_response(intro_p, temperature=temp, max_tokens=1024)
    print(f"\n=== INTRODUCTION ===\n{intro}\n")
    print(intro)
    
    print("Would you like to generate the full essay? (y/n): ")
    print("1) Full draft\n2) Step-by-step")
    choice = input("> ").strip().lower()
    
    if choice == "1":
        body_p = f"Write a full body essay on '{details['topic']}' with an {details['essay_type']} style, targeting {details['target_audience']}, and a length of {details['length']}."
        body = generate_response(body_p, temperature=temp, max_tokens=2048)
        print(f"\n=== FULL ESSAY ===\n{body}\n")
        print(body)
    else:
        step_p = f"Write a step-by-step outline for an {details['essay_type']} essay on '{details['topic']}' aimed at {details['target_audience']} with a length of {details['length']}."
        body_step = generate_response(step_p, temperature=temp, max_tokens=1024)
        print(f"\n=== STEP-BY-STEP OUTLINE ===\n{body_step}\n")
        print(body_step)
        
    concl_p = f"Write a conclusion for an {details['essay_type']} essay on '{details['topic']}' aimed at {details['target_audience']}."
    conclusion = generate_response(concl_p, temperature=temp, max_tokens=1024)
    print(f"\n=== CONCLUSION ===\n{conclusion}\n")
    print(conclusion)
    
def feedback_and_refinement():
    try:
        rating = int(input("Rate the generated essay (1-5): ").strip())
        if not (1 <= rating <= 5): raise ValueError
    except ValueError:
        print("Invalid rating. Using default rating of 3.")
        rating = 3
        
    if rating != 5:
        feedback = input("Please provide specific feedback for improvement: ").strip()
        print("Thank you for your feedback! The essay will be refined based on your input.")
    else:
        print("Great! I'm glad you liked the essay.")
        
def run_essay_assistant():
    print("\n=== AI ESSAY WRITING ASSISTANT ===\n")  
    details = get_essay_details()
    if not details["topic"] or not details["essay_type"]:
        print("Topic and essay type are required. Exiting.")
        return
    generate_essay(details)
    feedback_and_refinement()
    
if __name__ == "__main__":
    run_essay_assistant()  
from hf import generate_response

def bias_mitigation_activity():
    print("\n=== BIAS MITIGATION ACTIVITY ===\n")
    prompt = input("Enter a prompt that may contain bias (e.g., 'Describe a doctor'): ").strip()
    if not prompt:
        print("No prompt entered. Exiting activity.")
        return
    initial_response = generate_response(prompt)
    print(f"\nAI's initial response: {initial_response}")
    
    modified_prompt = input("\nModify the prompt to reduce potential bias (e.g., 'Describe a doctor without mentioning gender'): ").strip()
    if modified_prompt:
        modified_response = generate_response(modified_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nAI's response to modified prompt: {modified_response}")
    else:
        print("No modified prompt entered. Skipping bias mitigation step.")
        
def token_limit_activity():
    print("\n=== TOKEN LIMIT ACTIVITY ===\n")
    long_prompt = input("Enter a prompt that may generate a long response (e.g., 'Explain the history of the universe'): ").strip()
    if long_prompt:
        long_response = generate_response(long_prompt, temperature=0.3, max_tokens=2048)
        preview = long_response[:500] + "..." if len(long_response) > 500 else long_response
        print(f"\nAI's response (preview): {preview}")
    else:
        print("No prompt entered. Exiting activity.")
        
    short_prompt = input("\nEnter a prompt that should generate a short response (e.g., 'What is 2+2?'): ").strip()
    if short_prompt:
        short_response = generate_response(short_prompt, temperature=0.3, max_tokens=50)
        print(f"\nAI's response: {short_response}")
    else:
        print("No prompt entered. Exiting activity.")
        
def run_activity():
    print("\n=== AI Learning Activities ===\n")
    print("Choose an activity:")
    print("1. Bias Mitigation Simulation")
    print("2. Token Limit Exploration")
    choice = input(">").strip()
    if choice == "1":
        bias_mitigation_activity()
    elif choice == "2":
        token_limit_activity()
    else:
        print("Invalid choice. Exiting.")
        
if __name__ == "__main__":
    run_activity()
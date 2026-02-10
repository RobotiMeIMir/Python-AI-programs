import requests
from colorama import Fore, Style, init

init(autoreset=True)
DEFAULT_MODEL = "google/pegasus-xsum"
def sum(model_name):
    return f"https://router.huggingface.co/models/{model_name}"
def query(payLoad, model_name=DEFAULT_MODEL): #payload is a dictionary that contains the input and paramiter of an API
    api_url = sum(model_name)
    headers = {"Authorization": f"Bearer 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"}
    response = requests.post(api_url, headers=headers, json=payLoad)
    return response.json()

def sum_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        }
    }
    print(Fore.GREEN + Style.BRIGHT + f"Summarizing text with model {model_name}")
    result = query(payload, model_name)
    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + Style.BRIGHT + "Error in summarization API response:")
        print(result)
        return None
    
if __name__ == "__main__":
    print(Fore.GREEN + Style.BRIGHT + "Hi, what's your name?")
    name = input("Name: ").strip()
    
    if not name:
        name = "Rock"
        
    print(Fore.BLACK + Style.BRIGHT + f"Welcome, {name}!")
    
    user_text = input(Fore.BLUE + Style.BRIGHT + "Enter text to summarize: ").strip()
    if not user_text:
        print(Fore.RED + Style.BRIGHT + "No text entered. Exiting.")
    else:
        print("Enter the model name you want to use.")
        model_choice = input("Model (default: google/pegasus-xsum): ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL
            print("Chose3 your summery style. 1,4 or 2,4 to enhance the summary.") 
            style_choice = input("Style (default: 1,4): ").strip()
            if style_choice == "2":
                min_len, max_len = 50, 200
                print("Enhanced memor, processed.")
            else:
                min_len, max_len = 50, 150
                print("Summarizing, processed.")
                
            summary = sum_text(user_text, min_len, max_len, model_choice)
            if summary:
                print(Fore.GREEN + Style.BRIGHT + f"AI Summary Generated: {summary}")
                print(summary)
            else:
                print(Fore.RED + Style.BRIGHT + "Failed to generate summary.")
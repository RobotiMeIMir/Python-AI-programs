import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init()

print(f"{Fore.CYAN} Welcome to AI! {Style.RESET_ALL}")

user_name = input(f"{Fore.MAGENTA} Enter your name: {Style.RESET_ALL} ").strip()
if not user_name:
    user_name = "Detective"
conversation_history =[] 
print(f"\n{Fore.CYAN}Hello, Detective {user_name}!")

print(f"Type a Sentence and I will analyze your sentences with TextBlob and show you the sentiment. 🧠")

print(f"Type {Fore.YELLOW}'reset'{Fore.CYAN}, {Fore.YELLOW}'history'{Fore.CYAN}, or {Fore.YELLOW}'exit'{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()
    if user_input.lower() == "exist":
        print(f"\n{Fore.BLUE} Exciting Statement Detective. {user_name} {Style.RESET_ALL}")
        break
    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.CYAN} All the conversation is cleared {Style.RESET_ALL}")
        continue
    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.CYAN}No conversation history yet.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN} Conversation History: {Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == "Positive":
                    color= Fore.GREEN
                    emoji= "😁"
                elif sentiment_type == "Negative":
                    color= Fore.RED
                    emoji= "😁"
                else:
                    color= Fore.YELLOW
                    emoji= "😁"
                print(f"{idx}. {color}{emoji} {text}"
                      f"(Polarity: {polarity: .2f}, {sentiment_type}){Style.RESET_ALL}")
                
            continue
        polarity = TextBlob(user_input).sentiment.polarity #statement analizing
        
        if polarity > 0.25:
           sentiment_type = "Positive"
           color = Fore.GREEN
           emoji = "😊"
        elif polarity < -0.25:
           sentiment_type = "Negative"
           color = Fore.RED
           emoji = "😞"
        else:
           sentiment_type = "Neutral"
           color = Fore.YELLOW
           emoji = "😐"
           
    conversation_history.append((user_input, polarity, sentiment_type))
    
    print(f"{color}{emoji} {sentiment_type} sentiment detected! "
          f"(Polarity: {polarity: .2f}) {Style.RESET_ALL}")
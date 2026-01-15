import requests
def pff_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        joke = response.json()
        print(f"{joke['setup']} - {joke['punchline']}")
    else:
        print("Failed to retrieve a joke.")
def main():
    print("Welcome Everybody!!")
    while True:
        user_input = input("Type 'joke' to hear a joke or 'exit' to quit: ").strip().lower()
        if user_input in ("exit", "quit"):
            print("Goodbye!")
            break
        joke = pff_joke()
        print(joke)
if __name__ == "__main__":
    main()
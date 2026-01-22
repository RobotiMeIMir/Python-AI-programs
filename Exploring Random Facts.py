import requests
url = "https://uselessfacts.jsph.pl/random.json?language=en"
def fetch_technology_fact():
    response = requests.get(url)
    if response.status_code == 200: #200 shows that the request was successful
        data = response.json()
        return data['id'][0]['text']
    else:
        print("Cannot fetch the data.")
        
while True:
    user_input = input("Press enter to get a random technology fact or type q to quit: ")
    if user_input.lower() == 'q':
        break
    fetch_technology_fact()
import requests
from PIL import Image
from io import BytesIO
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers"

def images(prompt: str)-> Image.Image:
    header = {"Authorization": f"Bearer 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"}
    payload = {"Inputs": prompt}
    try: 
        response = requests.post(API_URL, headers=header, json=payload, timeout=30)
        response.raise_for_status()
        if "image" in response.headers.get("Content_Type", ""):
            image = Image.open(BytesIO(response.content)) 
            return image
        else:
            raise Exception("Sorry, there seems to be an error!")
    except requests.exceptions.RequestException as E:
        raise Exception("There seems to be an error!", E)
    
def main():
    print("Welcome to Image Generating!")
    print("Type 'Exit' to quit.")
    
    while True:
        prompt =  input("Describe any image that you want to create!").strip()
        if prompt.lower()=="exit":
            print("Goodbye!")
            break
        print("Image Generating..")
        try:
            image = images(prompt)
            image.show()
            opinion = input("Do you want to save it?").strip().lower()
            if opinion == "yes":
                file_name = input("Enter file name").strip() or "Generated Image" 
                file_name = "".join(c for c in file_name if c.isalnum() or c in ('_', '-')).rstrip()
                image.save(f"{file_name}.png")
                print("Your file was successfully saved!")
        except Exception as E:
            print(E)
            
if __name__ == "__main__": #makes it start from the main function
    main()
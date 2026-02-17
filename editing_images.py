import requests
import time
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from colorama import Fore, Style

MODELS = [
"runwayml/stable-diffusion-v1-5",
"stabilityai/stable-diffusion-2-1",
"prompthero/openjourney",
]
HEADERS = {"Authorization": f"Bearer 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", "Content-Type": "application/json", "Accept": "image/png"}
def image(prompt): #for safe call back generation
    payload, last_error = {"inputs": prompt}, None
    for model in MODELS:
        url = f"https://router.huggingface.co/hf-inference/models/{model}"
        for _ in range(3):
            r = requests.post(url, headers=HEADERS, json=payload, timeout=90)
            cp = (r.headers.get("Content-Type") or "").lower()
            if r.status_code == 503 and "application/json" in cp:
                try:
                    e = int(r.json().get("estimated_time", 0))
                except Exception:
                    e = 10
                time.sleep(e)
                continue
            if r.status_code == 200 and "application/json" in cp:
                try:
                    return Image.open(BytesIO(r.content)).convert("RGB")
                except Exception as E:
                    last_error = E
                    break
            try: 
                body = r.json() if "application/json" in cp else r.text
            except Exception as E:
                body = r.text
                last_error = E
                break
        raise Exception(f"Failed to generate image with all models. Last error: {last_error}, Last response: {body}")
def post(image):
    image= ImageEnhance.Brightness(image).enhance(1.2)
    image= ImageEnhance.Contrast(image).enhance(1.3)
    return image.filter(ImageFilter.SHARPEN)
def main():
    print(Fore.BLUE + "Welcome to the Image Editor! Type 'Exit' to quit.")
    
    while True:
        prompt = input("Describe an image you want to create: ").strip()
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        try:
            print("Generating image...")
            img = image(prompt)
            psd = post(img)
            psd.show()
            save = input("Do you want to save the edited image? (yes/no): ").strip().lower()
            if save == "yes":
                file_name = input("Enter a file name (without extension): ").strip() or "edited_image"
                file_name = "".join(c for c in file_name if c.isalnum() or c in ('_', '-')).rstrip()
                psd.save(f"{file_name}.png")
                print("Image saved successfully!")
        except Exception as E:
            print(Fore.RED + f"Error: {E}" + Style.RESET_ALL)
if __name__ == "__main__":
    main()
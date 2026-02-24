import requests
import base64
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer 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", "Content-Type": "application/json"}
MODELS = [
"Qwen/Qwen3-VL-8B-Instruct:together",
"Qwen/Qwen3-VL-32B-Instruct:together",
"Qwen/Qwen2.5-VL-32B-Instruct:together",
"Qwen/Qwen2-VL-7B-Instruct:together",
]

def img(b: bytes) ->str: #makes the output of the image in bytes to a string
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")

def error_msg(r: requests.Response) -> str:
    try:
        return r.json().get("error", "Unknown error")
    except Exception:
        return f"Failed to parse error message. Status code: {r.status_code}, Response: {r.text}"   
    
def box(title: str, lines: list[str], icon: str) -> str:
    m = max(30, len(title) + 4, *(len(x) for x in lines) )
    print("+" + "-" * m + "+")
    for x in lines:
        print("| " + x.ljust(m) + " |")
        
def cap_sing_img():
    image_source = input("Enter the file name or URL of the image: ").strip() or "Text.jpg"
    try:
        with open(image_source, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        print("Error reading image file:", e)
        return
    base = { "messages": [{"role": "user","content": [{"type": "text", "text": "Give a short caption for this image."},{"type": "image_url", "image_url": {"url": img(image_bytes)}},],}],"max_tokens": 60,"temperature": 0.2,}
    last  = None
    for model in MODELS:
        payload={**base, "model": model}
        try:
            r =requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
        except Exception as e:
            print(f"Error making request to model {model}:", e)
            continue
        if r.status_code != 200:
            last = error_msg(r)
            continue
        try:
            p = r.json()
        except Exception as e:
            print(f"Error parsing response from model {model}:", e)
            continue
        cap = p.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if cap:
            box(f"Model: {model}", [cap], "🖼️")
            return
        last = "Mo caption found"
        box(f"Model: {model}", [last], "⚠️")
        
def main():
    cap_sing_img()
if __name__ == "__main__":
    main()
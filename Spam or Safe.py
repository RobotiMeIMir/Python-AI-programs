import requests
import os
from dotenv import load_dotenv

# Load your Hugging Face token from environment (e.g., .env file with HF_TOKEN=Sword)
load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')  # Replace with your actual token if not using .env

MODEL_ID = "facebook/bart-large-mnli"  # Using zero-shot classification like the example
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
CATEGORIES = ["Spam", "Safe"]  # Changed from topics to spam/safe classification

def ask_hf(text: str):
    payload = {"inputs": text, "parameters": {"candidate_labels": CATEGORIES}}
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(f"HF error {r.status_code}: {r.text}")
    return r.json()  # returns a LIST of {"label": ..., "score": ...}

def best_category(preds: list):
    best = max(preds, key=lambda x: x["score"])
    return best["label"], best["score"]

def bar(score: float) -> str:
    pct = score * 100
    blocks = int(pct // 10)
    return "█" * blocks + "░" * (10 - blocks)

def show(text: str, preds: list):
    top_label, top_score = best_category(preds)
    print("\n" + "=" * 60)
    print("🛡️ Text Spam/Safe Classifier")
    print("=" * 60)
    print("Text:", text)
    print(f"Best classification: {top_label}")
    print(f"Confidence: {round(top_score*100,1)}% [{bar(top_score)}]")

    print("\nTop 2 guesses:")
    top2 = sorted(preds, key=lambda x: x["score"], reverse=True)[:2]  # Only 2 categories, so top 2
    for i, p in enumerate(top2, start=1):
        print(f"{i}. {p['label']:<6} {round(p['score']*100,1)}% [{bar(p['score'])}]")
    print("=" * 60)

def main():
    print("Welcome! Type a text and I'll classify it as Spam or Safe.")
    print("Categories:", ", ".join(CATEGORIES))
    print("Type 'exit' to stop.\n")

    while True:
        text = input("Text: ").strip()
        if text.lower() == "exit":
            print("Bye! Keep coding 🚀")
            break
        if not text:
            print("Please type some text (not empty).\n")
            continue
        try:
            preds = ask_hf(text)
            if isinstance(preds, list) and preds and "label" in preds[0]:
                show(text, preds)
            else:
                print("Oops! Unexpected reply:", preds)
        except Exception as e:
            print("\n⚠️ Oops! Something went wrong.")
            print("Reason:", e)
            print("Tip: Check HF_TOKEN + internet.\n")

if __name__ == "__main__":
    main()
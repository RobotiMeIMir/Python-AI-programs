from io import BytesIO
import requests
import streamlit as st
from huggingface_hub import InterfaceClient
import config

MODEL_ID = "stabilityai/stable-diffusion-3-medium-diffusers"
FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"

ENHANCE_SYS = ("Improve the quality of the image by enhancing details, colors, and overall clarity. ")

NEGATIVE = "low quality, blurry, pixelated, overexposed, underexposed, noisy, artifacts, distorted, poorly lit, bad composition"
img_client = InterfaceClient(provider="hf-interference", api_key=config.API_KEY)

def check_prompt_w_filter_api(prompt: str):
    try:
        response = requests.post(
            FILTER_API_URL,
            json={"prompt": prompt},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if not isinstance(data, dict):
            return {"ok": False, "reason": "Invalid response format from filter API."}
        return data
    except Exception as e:
        return {"ok": False, "reason": f"Error calling filter API: {str(e)}"}
    
def enhance_prompt(raw: str) -> str:
    from hf import generate_response
    
    out = generate_response(f"{ENHANCE_SYS}\nUser prompt: {raw}", temperature=0.4, max_tokens=220)
    return (out or raw).strip()

def generate_image(prompt: str):
    filter_result = check_prompt_w_filter_api(prompt)
    if not filter_result.get("ok"):
        return None, f"Prompt rejected by filter API: {filter_result.get('reason', 'Unsafe content detected.')}"
    
    try:
        return img_client.text_to_image(prompt=prompt, negative_prompt=NEGATIVE, model=MODEL_ID), None
    except Exception as e:
        msg = str(e)
        
        if "negative_prompt" in msg or "unexpected keyword argument 'negative_prompt'" in msg:
            try:
                return img_client.text_to_image(prompt=prompt, model=MODEL_ID), None
            except Exception as e2:
                msg = str(e2)
    
    if any(x in msg for x in ["Content filter", "NSFW content detected", "Prompt rejected"]):
        return None, "Prompt rejected by content filter. Please modify your prompt and try again." + msg
    if "404" in msg or "Not Found" in msg:
        return None, "Model not found. Please check the model ID and try again." + msg
    if "404" in msg or "Not Found" in msg:
        return None, "Model not found. Please check the model ID and try again." + msg
    return None, "Error generating image: " + msg

def main():
    st.set_page_config(page_title="Image Generation", layout="centered")
    st.title("Image Generation with Stable Diffusion")
    st.write("Enter a prompt to generate an image. The model will enhance your prompt for better results.")
    
    with st.form("image_form"):
        raw = st.text_area("Image Description", height=120, placeholder="e.g. A serene landscape with mountains and a river at sunset.")
        submit = st.form_submit_button("Generate Image")
        
        if submit:
            raw = raw.strip()
            if not raw:
                st.warning("Please enter a description for the image.")
                return
            raw_check = check_prompt_w_filter_api(raw)
            if not raw_check.get("ok"):
                st.error(f"Prompt rejected by filter API: {raw_check.get('reason', 'Unsafe content detected.')}")
                return
            
            with st.spinner("Enhancing prompt..."):
                enhanced_prompt = enhance_prompt(raw)
                
            enhanced_check = check_prompt_w_filter_api(enhanced_prompt)
            if not enhanced_check.get("ok"):
                st.error(f"Enhanced prompt rejected by filter API: {enhanced_check.get('reason', 'Unsafe content detected.')}")
                return
            st.markdown("### Enhanced Prompt")
            st.code(enhanced_prompt)
            
            with st.spinner("Generating image..."):
                image, error = generate_image(enhanced_prompt)
            if error:
                st.error(error)
                return
            st.image(image, caption="Generated Image", use_container_width=True)
            st.session_state.generated_image = image
            
        img = st.session_state.get("generated_image")
        if image:
            buf = BytesIO()
            image.save(buf, format="PNG")
            st.download_button("Download Image", buf.getvalue(), "ai_generated_image.png", "image/png")
if __name__ == "__main__":
    main()
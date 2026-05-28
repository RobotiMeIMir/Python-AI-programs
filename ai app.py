import io, re
from io import BytesIO
import streamlit as st
from huggingface_hub import InterfaceClient
import config
from groq import generate_response

MATH_SYSTEM = """You are a math assistant that can solve math problems step by step.
When given a math problem, you will break it down into smaller steps and solve each step one by one."""

CHAT_CSS = """
<style>
.wrap {max-height: 520px; overflow-y: auto; padding-right: 6px}
.card{border:1px solid #e6e6e6; background:fff; border-radius: 8px; padding: 10px; margin-bottom: 14px 16px; margin: 10px 0;
box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
.q{font-weight: 500; color: #333;margin-bottom: 8px;}
.meta{display: inline-block; background:#FFF2E5; color: #FF6B00; font-size: 12px; padding: 2px 6px; border-radius: 4px;
margin-bottom: 8px;}
.a{white-space: pre-wrap; color: #555; line-height:1.5}
</style>
"""

def export_txt(history):
    txt = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history, 1)])
    bio = io.BytesIO(txt.encode("utf-8")); bio.seek(0)
    return bio

def teaching_answer(q: str) -> str:
    prompt = f"{MATH_SYSTEM}\n\nDifficulty: {level}\nUser question: {q}"
    return generate_response(prompt, temperature=0.4, max_tokens=512)

def run_ai_teaching_assistant():
    st.title("AI Teaching Assistant")
    st.session_state.setdefault("history_ata", [])
    c1, c2 = st.columns([1, 2])
    if c1.button("Clear", key = "c_ata"): st.session_state.history_ata = [];
st.rerun()
    if st.session_state.history_ata:
        c2.download_button("Export History", export_txt(st.session_state.history_ata), "AI_teaching_assistant_history.txt", "text/plain")
    q = st.text_input("Enter a math problem or question:")
    if st.button("Ask", key="ask_ata"):
        if not q.strip():
            st.warning("Please enter a valid question.")
        else:
            with st.spinner("Generating answer..."):
                st.session_state.history_ata.append({"question": q.strip(), "answer": teaching_answer(q)})
                st.rerun()
    if not st.session_state.history_ata: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_ata, 1):
        html += f'<div class="card"><div class="q">Q{i}: {qa["question"]}</div><div class="a">{qa["answer"]}</div></div>'
    st.markdown(html + '</div>', unsafe_allow_html=True)
    
def run_math_sorcerer():
    st.title("Math Sorcerer")
    st.session_state.setdefault("history_mm", [])
    st.session_state.setdefault("k_mm", 0)
    c1, c2 = st.columns([1, 2])
    if c1.button("Clear", key = "c_mm"): st.session_state.history_mm = [];
st.rerun()
    if st.session_state.history_mm:
        c2.download_button("Export History", export_txt(st.session_state.history_mm), "Math_Sorcerer_history.txt", "text/plain")
    q = st.text_area("Math problem: ", height = 100, key = f"mm_{st.session_state.k_mm}")
    a, b = st.columns([3, 1])
    go = a.form_submit_button("Solve", use_container_width=True)
    lvl = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
    if go:
        if not q.strip():
            st.warning("Please enter a valid math problem.")
        else:
            with st.spinner("Solving..."):
                ans = math_answer(q.strip(), lvl)
            st.session_state.history_mm.insert(0, {"question": q.strip(), "answer": ans, "difficulty": lvl})
            st.session_state.k_mm +=1; st.rerun()
            
    if not st.session_state.history_mm: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_mm, 1):
        html += (f'<div class="card"><div class="q">Q{i}: {qa["question"]}'
                f' <span class="meta">{qa["difficulty"]}</span></div><div'
                f'class="a">{qa["answer"]}</div></div>')
    st.markdown(html + '</div>', unsafe_allow_html=True)
    
def run_safe_ai_image_gen():
    FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"
    IMG_MODEL ="stabilityai/stable-diffusion-x1-base-1.0"
    img_client = InterferenceClient(provider ="hf_interference", api_key = config.HF_API_KEY)
    st.title("Safe AI Image Generator")
    
    def is_prompt_safe(prompt:str):
        try:
            response = requests.post(
                FILTER_API_URL,
                json={"text": prompt},
                timeout=15
            )
            
            if response.status_code != 200:
                return False, f"Filter API failed with status {response.status_code}: {response.text}"
            
            data = response.json()
            if data.get("ok") is True:
                return True, None
            return False, data.get("reason", "Unsafe prompt")
        except Exception as e:
            return False, f"Filter API error: {e}"
        
    def generate_image(prompt:str):
        safe, err = is_prompt_safe(prompt)
        if not safe:
            return None, err
        try:
            image =img_client.text_to_image(prompt=prompt, model=IMG_MODEL)
            return image, None
        except Exception as e:
            return None, f"Image generation error: {e}"
        
    with st.form("img_form"):
        p = st.text_area("Image description: ", height = 120)
        ok = st.form_submit_button("Generate Image")
    if ok:
        if not p.strip():
            st.warning("Please enter a valid image description.")
        else:
            with st.spinner("Generating image..."):
                img, error = generate_image(p.strip())
            if error:
                st.error(error)
            else:
                st.image(img, use_container_width=True)
                st.session_state.generated_image = img
                
    img = st.session_state.get("generated_image")
    if img:
        buf = BytesIO(); 
        img.save(buf, format="PNG")
        st.download_button("Download Image", buf.getvalue(), "generated_image.png", "image/png")
        
        
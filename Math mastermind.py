from hf import generate_response
import io, streamlit as st
SYSTEM_PROMPT = """You are a math mastermind, a genius mathematician who can solve any math problem with ease. 
For every math problem: 1) Show step-by-step solution, 2) Provide the final answer, 3) Explain the reasoning behind each step in a clear and concise manner.
Format: Problem -> Step-by-step solution -> Final answer -> Explanation of reasoning.
"""
def solve_math_problem(problem: str, level: str, temperature = 0.1, max_tokens=1024)-> str:
    prompt = f"{SYSTEM_PROMPT}\n\nProblem ({level}): {problem}"
    return generate_response(prompt, temperature=temperature, max_tokens=max_tokens)

def export_txt(history):
    text = "\n\n".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}" for i, h in enumerate(history, 1)])
    return io.BytesIO(text.encode("utf-8"))

def set_up_ui():
    st.set_page_config(page_title="Math Mastermind", layout="centered")
    st.title("Math Mastermind")
    st.write("Ask me any math problem, and I'll solve it step by step!")
    
    with st.expander("Examples"):
        st.markdown(
            '-Algebra: "Solve 3x + 5 = 20 for x."\n'
            '-Calculus: "Find the derivative of f(x) = 2x^3 + 5x^2 - 3x + 7."\n'
            '-Geometry: "Calculate the area of a circle with radius 5."\n'
            '-Probability: "What is the probability of rolling a sum of 7 with two dice?"\n'
        )
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", "0")
    
    c1, c2 = st.columns([1, 2])
    if c1.button("Clear History"):
        st.session_state.history = []; st.rerun()
        
    if st.session_state.history:
        c2.download_button("Export", export_txt(st.session_state.history), "math_mastermind_history.txt", "text/plain")
        
    with st.form("math_form", clear_on_submit=True):
        q = st.text_area("Enter your math problem:", height=100, placeholder="e.g. Solve 3x + 5 = 20 for x.", key=f"q{st.session_state.k}")
        a, b = st.columns([3, 1])
        solve = a.form_submit_button("Solve", use_container_width=True)
        level = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
        
        if solve:
            if not q.strip(): st.warning("Please enter a math problem.")
            else:
                with st.spinner("Solving..."):
                    answer = solve_math_problem(q.strip(0), level)
                st.session_state.history.insert(0, {"question": q, "answer": answer})
                st.session_state.k += 1
                st.rerun()
                
        if not st.session_state.history: return
        st.markdown("### Solution History")
        st.markdown("""<style>
        .box{max-height:500px;overflow-y:auto;border:2px solid #e6e6e6;background:#f9f9f9;border-radius:10px;padding:10px;margin:10px 0;box-shadow:0 1px 2px rgba(0,0,0,0.04);}
        .q{font-weight:700;color:#0a6ebd;margin-bottom:8px;}
        .lvl{display:inline-block;background:#0a6ebd;color:#fff;padding:2px 6px;border-radius:4px;font-size:12px;margin-left:10px;}
        radius: 12px;font-size: 14px;line-height: 1.5;}
        radius:8px;font-size:12px;line-height:1.5;}
        </style>""", unsafe_allow_html=True)
        
        html = '<div class="box">'
        for i, h in enumerate(st.session_state.history, 1):
            html += f'<div class="q">Q{i}: {h["question"]}<span class="lvl">{level}</span></div>'
            html += f'<div class="a">A{i}: {h["answer"]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)
        
if __name__ == "__main__":
    set_up_ui()
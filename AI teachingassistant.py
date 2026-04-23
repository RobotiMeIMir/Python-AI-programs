from groq import generate_response

import reimport streamlit as st

def looks_incomplete(text:str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t = text.strip()
    
    if t.endswith(("**", "*", "-", "_", ",", ":", ";", "(", "[", "{", "\"", "'")):
        return True
    if re.search(r"\d+\.\s*\*", t):
        return True
    if not re.search(r"[.!?…](['\"\)\]\}]?\s*$)", t):
        return True
    return False

def complete_answer(question: str, max_rounds: int = 2) -> str:
    base_prompt = (
        "Answer in numbered points."
        "Do not cut sentences. Finish each point completely before moving to the next."
        f"Question: {question}"
    )

    ans = generate_response(base_prompt, temperature=0.3, max_tokens=1024)

    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):     
        cont_prompt = (          
            "Continue the answer, starting from where you left off. Do not repeat previous points."
            "Do not repeat any part of the previous answer. Finish the current point before moving to the next."
            "Finish the incomplete point and continue with the next ones, if any."
            f"Question: {question}\n\n"
            f"Answer so far:\n{ans}\n\nContinue the answer:"
        )
    
    MORE = generate_response(cont_prompt, temperature=0.3, max_tokens=1024)
    if not more or more.strip() in ans:
        break
    ans = (ans.rstrip() + "\n" + more.strip()).strip()
    rounds += 1

    return ans

def main():
    st.title("AI Teaching Assistant")
    st.write("Ask any question and get a detailed answer in numbered points. The assistant will ensure complete answers, even if it takes multiple rounds.")
    
    user_input = st.text_input("Enter your question:")
    
    if user_input:
       st.write(f"**Your question:** {user_input}")
       response = complete_answer(user_input)
       st.write("**AI Teaching Assistant's answer:**")
       st.markdown(response)
    else:
        st.info("Please enter a question to get started.")
    
if __name__ == "__main__":    main()
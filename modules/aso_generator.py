import collections
import re
import ollama

def extract_pure_python_keywords(text: str):
    """
    Zero-dependency offline analyzer. Extracts high-density keywords 
    by counting frequencies and filtering out noise words.
    """
    words = re.findall(r'\b\w{4,}\b', text.lower())
    stop_words = {'this', 'that', 'with', 'from', 'your', 'have', 'features', 'apps', 'application', 'user', 'users'}
    filtered_words = [w for w in words if w not in stop_words]
    most_common = collections.Counter(filtered_words).most_common(12)
    return ", ".join([word for word, count in most_common])

def generate_keywords(text: str, gemini_key: str = None, model: str = "llama3"):
    """
    Multi-stage fallback strategy to eliminate setup friction for users.
    """
    # Stage 1: Try local Ollama instance
    try:
        prompt = f"Extract the top 10 App Store Optimization (ASO) keywords from this text:\n\n{text}"
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content'], "Ollama (Local AI)"
    except Exception:
        pass

    # Stage 2: Try Cloud Gemini API if a free key is provided
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Extract the top 10 App Store Optimization (ASO) keywords from this text. Provide them in a neat bulleted list:\n\n{text}"
            response = gemini_model.generate_content(prompt)
            return response.text, "Gemini API (Cloud AI)"
        except Exception as e:
            return f"⚠️ Attempted Gemini Cloud fallback but failed: {e}", "Error"

    # Stage 3: Zero-config Native Rule Engine
    fallback_keywords = extract_pure_python_keywords(text)
    user_tip = (
        f"### 💡 Suggested Core Keywords:\n`{fallback_keywords}`\n\n"
        f"--- \n"
        f"*Pro-Tip: Get advanced AI definitions by running Ollama locally or pasting a free "
        f"Gemini API key into the side panel!*"
    )
    return user_tip, "Offline Analyzer (No Setup Required)"

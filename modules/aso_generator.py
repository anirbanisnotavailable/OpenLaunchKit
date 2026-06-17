import ollama

def generate_keywords(text: str, model: str = "llama3"):
    """
    Calls local Ollama instance to extract keywords.
    """
    prompt = f"Extract the top 10 App Store Optimization (ASO) keywords from this text:\n\n{text}"
    try:
        response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to Ollama: {e}. Please ensure it is running."

import os
import google.generativeai as genai

# Configure API for Google's generative AI
gemini_api_key = os.getenv("GEMINI_PRO_KEY")
genai.configure(api_key=gemini_api_key)

def generate_answer_from_context(query, context):
    """Generates a response based on a user's query and provided context using a language model."""
    model = genai.GenerativeModel('gemini-pro')
    instruction = (
        "Provide a detailed and accurate response based on the context given. "
        "If the context is insufficient for a comprehensive answer, request more details. "
        "Ensure your response is grounded in the provided information."
    )
    prompt = f"Instructions: {instruction} \n\nContext: {context}\n\nQuery: {query}"
    response = model.generate_content(prompt)
    return response.text

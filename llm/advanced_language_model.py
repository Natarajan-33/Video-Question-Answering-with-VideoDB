import os
import google.generativeai as genai
from typing import Any

# Configure API for Google's generative AI
gemini_api_key = os.getenv("GEMINI_PRO_KEY")
genai.configure(api_key=gemini_api_key)



safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


def generate_answer_from_context(query: str, context: str) -> Any:
    """
    Generates a response based on a user's query and the provided context using a language model.

    Args:
        query (str): The user's query.
        context (str): The context information to base the response on.

    Returns:
        Any: The generated response from the language model.
    """
    model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
    instruction = (
        "Provide a detailed and accurate response based on the context given. "
        "If the context is insufficient for a comprehensive answer, request more details. "
        "Ensure your response is grounded in the provided information."
    )
    prompt = f"Instructions: {instruction} \n\nContext: {context}\n\nQuery: {query}"
    response = model.generate_content(prompt)
    return response.text

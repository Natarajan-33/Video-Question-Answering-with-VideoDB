import os
import google.generativeai as genai
from typing import Any
import logging
from dotenv import load_dotenv


# Load environment variables
try:
    load_dotenv(override=True)
    gemini_api_key = os.getenv("GEMINI_PRO_KEY")
    if gemini_api_key:
        # Configure API for Google's generative AI
        genai.configure(api_key=gemini_api_key)
        logging.info("API key configured successfully.")
    else:
        logging.error("GEMINI_PRO_KEY is not set in the environment variables.")
        # Raise an exception to halt execution
        raise RuntimeError("API key configuration failed.")
    
except Exception as e:
    logging.error(f"Error loading environment variables or configuring API key. error={e}")
    raise  # Re-raise the exception to halt execution


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
    try:
        model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
        instruction = (
            "Provide a detailed and accurate response based on the context given. "
            "If the context is insufficient for a comprehensive answer, request more details. "
            "Ensure your response is grounded in the provided information."
        )
        prompt = f"Instructions: {instruction} \n\nContext: {context}\n\nQuery: {query}"
        response = model.generate_content(prompt)
        logging.info("LLM responded successfully. fn=generate_answer_from_context")
        return response.text
    except Exception as e:
        logging.error(f"Error occured while generating response from LLM. fn=generate_answer_from_context,error={e}")
        raise e


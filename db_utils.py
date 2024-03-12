import streamlit as st
from videodb import connect
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

gemini_api_key = os.getenv("GEMINI_PRO_KEY")
videodb_api_key = os.getenv("VIDEODB_KEY")


genai.configure(api_key=gemini_api_key)

conn = connect(api_key=videodb_api_key)
coll = conn.get_collection()

# Function to upload videos
def upload_videos_to_database(youtube_links):
    for link in youtube_links:
        try:
            coll.upload(url=link)
            print(f"Video: {link} uploaded successfully")
            for video in coll.get_videos():
                video.index_spoken_words()
                print(f"Indexed {video.name}")
        except Exception as e:
            print(f"Exception occured for video {link} as {e}")

def getanswer(query):
    result = coll.search(query = query)
    print(result)
    print("Type: ")
    first_shot = result.get_shots()[0]
    video_title = first_shot.video_title
    text = first_shot.text
    answer = ""
    answer = call_llm(query, text)
    matching_video = {
        "video_title": video_title,
        "text": text
    }
    return answer, matching_video


# Create a prompt by combining the user query with the retrieved context.
def call_llm(query, context):
    model = genai.GenerativeModel('gemini-pro')
    # header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    header = "Please carefully respond to the prompts based on the provided context. Be truthful and specific in your answers. If the given context is insufficient to address a prompt, kindly request additional clarification from the user. Avoid making assumptions or providing inaccurate information. Your cooperation ensures the accuracy and relevance of the responses. Never provide information that is not grounded in the available context."
    prompt = f"Assistant behavior : {header} \n\n Provided context : {context}  \n\n  User Prompt : {query} "
    response = model.generate_content(prompt)
    answer = response.text
    return answer

import os
import streamlit as st
from dotenv import load_dotenv
from videodb import connect, SearchType, play_stream

load_dotenv()

# Establish a connection to the video database
videodb_api_key = os.getenv("VIDEODB_KEY")
connection = connect(api_key=videodb_api_key)
# collection = connection.get_collection()

def add_videos_to_index(collection_name, youtube_urls):
    video_dict = {}
    collection = connection.create_collection(name =collection_name, description = collection_name)
    """Uploads videos to the database and indexes their spoken words."""
    for url in youtube_urls:
        try:
            video = collection.upload(url=url)
            video_dict[video.name] = video.id
            st.write(f"Video: {video.name}({url}) uploaded successfully.")
            
        except Exception as error:
            st.write(f"Failed to upload and index {url}. Error: {error}")
            return None , None
        
    for video in collection.get_videos():
        video.index_spoken_words()
        st.write(f"Indexed spoken words in: {video.name}.")
        
    return video_dict, collection

# def find_related_content_by_query(query):
#     """Searches the database for content similar to the query and returns the first result."""
#     try:
#         search_results = collection.search(query=query)
#         first_result = search_results.get_shots()[0]
#         return first_result.text, {"video_title": first_result.video_title, "text": first_result.text}
#     except Exception as error:
#         print(f"Search failed for query '{query}'. Error: {error}")
#         return "", {}
    

def chat_with_video(collection, video_id, query):
    try:
        video = collection.get_video(video_id)
        search_results = video.search(query=query)
        first_result = search_results.get_shots()[0]
        return first_result.text, {"video_title": first_result.video_title, "text": first_result.text}
    except Exception as error:
        print(f"Search failed for query '{query}'. Error: {error}")
        return "", {}


def stream_video(collection, video_id):
    # video = connection.upload(url=video_id)
    video = collection.get_video(video_id)
    video.generate_stream()
    video.play()

def watch_shorts(collection, video_id, topic):
    video = collection.get_video(video_id)
    # video.index_spoken_words()
    result = video.search(query=topic)
    return result

def transcribe_video(collection, video_id):
    video = collection.get_video(video_id)
    # get text of the spoken content
    # text_json = video.get_transcript()
    text = video.get_transcript_text()
    return text

def add_subtitles(collection, video_id):
    video = collection.get_video(video_id)
    # video.index_spoken_words()
    new_stream = video.add_subtitle()
    play_stream(new_stream)

def thumbnail(collection, video_id):
    video = collection.get_video(video_id)
    return video.generate_thumbnail()

def delete_video_from_index(collection, video_id):
    video = collection.get_video(video_id)
    video.delete()

def delete_all_videos_from_index(collection):
    # coll = connection.get_collection()
    for video in collection.get_videos():
        video.delete()


def show_collection(collection):
    videos_list = []
    # coll = connection.get_collection()
    for video in collection.get_videos():
        videos_list.append(video)
    return videos_list

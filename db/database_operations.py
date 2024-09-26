import os
import streamlit as st
from dotenv import load_dotenv
from videodb import connect, SearchType, play_stream
from typing import List, Tuple, Dict, Optional
import streamlit as st

load_dotenv()

# Establish a connection to the video database
videodb_api_key = os.getenv("VIDEODB_KEY")
connection = connect(api_key=videodb_api_key)


def add_videos_to_index(collection_name: str, youtube_urls: List[str]) -> Tuple[Optional[Dict[str, str]], Optional[object]]:
    """
    Uploads videos to the database, indexes their spoken words, and returns a dictionary of video names to their IDs and the collection.

    Args:
        collection_name (str): The name of the collection to create.
        youtube_urls (List[str]): List of YouTube URLs to upload.

    Returns:
        Tuple[Optional[Dict[str, str]], Optional[object]]: A dictionary mapping video names to their IDs and the created collection. Returns (None, None) on failure.
    """
    video_dict = {}
    collection = connection.create_collection(name=collection_name, description=collection_name)
    
    with st.spinner('Uploading Videos...'):
        for url in youtube_urls:
            try:
                video = collection.upload(url=url)
                video_dict[video.name] = video.id
            except Exception as error:
                st.write(f"Failed to upload and index {url}. Error: {error}")
                return None, None
    
    with st.spinner('Indexing spoken words...'):
        for video in collection.get_videos():
            video.index_spoken_words()
            
    st.success(f"Video: {video.name}({url}) uploaded and indexed successfully.")
        
    return video_dict, collection

def chat_with_video(collection: object, video_id: str, query: str) -> Tuple[str, Dict[str, str]]:
    """
    Searches for related content within a specific video in the collection based on a query.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to search in.
        query (str): The search query.

    Returns:
        Tuple[str, Dict[str, str]]: The first result text and metadata. Returns empty string and dictionary on failure.
    """
    try:
        video = collection.get_video(video_id)
        search_results = video.search(query=query)
        first_result = search_results.get_shots()[0]
        return first_result.text, {"video_title": first_result.video_title, "text": first_result.text}
    except Exception as error:
        print(f"Search failed for query '{query}'. Error: {error}")
        return "", {}

def stream_video(collection: object, video_id: str) -> None:
    """
    Streams the video by generating a stream and playing it.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to stream.
    """
    video = collection.get_video(video_id)
    video.generate_stream()
    video.play()

def watch_shorts(collection: object, video_id: str, topic: str) -> object:
    """
    Searches for specific topics in the video and returns the result.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to search in.
        topic (str): The topic to search for in the video.

    Returns:
        object: The search result.
    """
    video = collection.get_video(video_id)
    result = video.search(query=topic)
    return result

def transcribe_video(collection: object, video_id: str) -> str:
    """
    Transcribes the video and returns the text of the spoken content.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to transcribe.

    Returns:
        str: The transcript text of the video.
    """
    video = collection.get_video(video_id)
    text = video.get_transcript_text()
    return text

def add_subtitles(collection: object, video_id: str) -> None:
    """
    Adds subtitles to the video and plays the new stream.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to add subtitles to.
    """
    video = collection.get_video(video_id)
    new_stream = video.add_subtitle()
    play_stream(new_stream)

def thumbnail(collection: object, video_id: str) -> object:
    """
    Generates a thumbnail for the video.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to generate a thumbnail for.

    Returns:
        object: The generated thumbnail.
    """
    video = collection.get_video(video_id)
    return video.generate_thumbnail()

def delete_video_from_index(collection: object, video_id: str) -> None:
    """
    Deletes a specific video from the index.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to delete.
    """
    video = collection.get_video(video_id)
    video.delete()

def delete_all_videos_from_index(collection: object) -> None:
    """
    Deletes all videos from the collection index.

    Args:
        collection (object): The video collection object.
    """
    for video in collection.get_videos():
        video.delete()

def show_collection(collection: object) -> List[object]:
    """
    Retrieves and returns a list of videos in the collection.

    Args:
        collection (object): The video collection object.

    Returns:
        List[object]: A list of videos in the collection.
    """
    videos_list = []
    for video in collection.get_videos():
        videos_list.append(video)
    return videos_list


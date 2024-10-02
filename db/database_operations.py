import os
import streamlit as st
from dotenv import load_dotenv
from videodb import connect, SearchType, play_stream
from typing import List, Tuple, Dict, Optional
import streamlit as st
from dotenv import load_dotenv
import os
import logging


# Load environment variables
try:
    load_dotenv(override=True)
    videodb_api_key = os.getenv("VIDEODB_KEY")
    
    if videodb_api_key:    
        # Establish a connection to the video database
        connection = connect(api_key=videodb_api_key)
        logging.info("API key configured successfully.")
    else:
        logging.error("VIDEODB_KEY is not set in the environment variables.")
        # Raise an exception to halt execution
        raise RuntimeError("API key configuration failed.")
    
except Exception as e:
    logging.error(f"Error loading environment variables or configuring API key. error={e}")
    raise  # Re-raise the exception to halt execution



def add_videos_to_index(collection_name: str, youtube_urls: List[str]) -> Tuple[Optional[Dict[str, str]], Optional[object]]:
    """
    Uploads videos to the database, indexes their spoken words, and returns a dictionary of video names to their IDs and the collection.

    Args:
        collection_name (str): The name of the collection to create.
        youtube_urls (List[str]): List of YouTube URLs to upload.
 
    Returns:
        Tuple[Optional[Dict[str, str]], Optional[object]]: A dictionary mapping video names to their IDs and the created collection. Returns (None, None) on failure.
    """
    try:
        video_dict = {}
        collection = connection.create_collection(name=collection_name, description=collection_name)
        
        with st.spinner('Uploading Videos...'):
            for url in youtube_urls:
                try:
                    video = collection.upload(url=url)
                    video_dict[video.name] = video.id
                    logging.info(f"Video: {video.name}({url}) uploaded successfully. fn=add_videos_to_index")
                except Exception as error:
                    st.write(f"Failed to upload and index {url}. Error: {error}")
                    logging.error(f"Error uploading and indexing video: {video.name}({url}). fn=add_videos_to_index, error={error}")
                    return None, None
        
        with st.spinner('Indexing spoken words...'):
            for video in collection.get_videos():
                video.index_spoken_words()
                
        st.success(f"Video: {video.name}({url}) uploaded and indexed successfully.")
        logging.info(f"Video: {video.name}({url}) uploaded and indexed successfully. fn=add_videos_to_index")
        return video_dict, collection
    
    except Exception as e:
        logging.error(f"Error uploading and indexing videos. fn=add_videos_to_index, error={e}")
        return None, None



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
        logging.info(f"Search on videodb is successful. fn=chat_with_video. video_id={video_id}, query={query}")
        return first_result.text, {"video_title": first_result.video_title, "text": first_result.text}
    except Exception as error:
        print(f"Search failed for query '{query}'. Error: {error}")
        logging.error(f"Search failed for query '{query}'. Error: {error}")
        return "", {}

def stream_video(collection: object, video_id: str) -> None:
    """
    Streams the video by generating a stream and playing it.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to stream.
    """
    try:
        video = collection.get_video(video_id)
        video.generate_stream()
        video.play()
        logging.info(f"Video streaming successful. fn=stream_video, video_id={video_id}")
    except Exception as e:
        logging.error(f"Error streaming video. fn=stream_video, video_id={video_id}, error={e}")
        raise e


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
    try:
        video = collection.get_video(video_id)
        result = video.search(query=topic)
        logging.info(f"Short videos search on videodb is successful. fn=watch_shorts. video_id={video_id}, topic={topic}")
        return result
    except Exception as e:
        logging.error(f"Short videos search on videodb is failed. fn=watch_shorts. video_id={video_id}, topic={topic}. error={e}")
        raise e


def transcribe_video(collection: object, video_id: str) -> str:
    """
    Transcribes the video and returns the text of the spoken content.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to transcribe.

    Returns:
        str: The transcript text of the video.
    """
    try:
        video = collection.get_video(video_id)
        text = video.get_transcript_text()
        logging.info(f"Video transcription successful. fn=transcribe_video, video_id={video_id}")
        return text
    except Exception as e:
        logging.error(f"Video transcription failed. fn=transcribe_video, video_id={video_id}. error={e}")
        raise e


def add_subtitles(collection: object, video_id: str) -> None:
    """
    Adds subtitles to the video and plays the new stream.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to add subtitles to.
    """
    try:
        video = collection.get_video(video_id)
        new_stream = video.add_subtitle()
        play_stream(new_stream)
        logging.info(f"Video with subtitles streaming successful. fn=add_subtitles, video_id={video_id}")
    except Exception as e:
        logging.error(f"Video with subtitles streaming failed. fn=add_subtitles, video_id={video_id}. error={e}")
        raise e



def thumbnail(collection: object, video_id: str) -> object:
    """
    Generates a thumbnail for the video.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to generate a thumbnail for.

    Returns:
        object: The generated thumbnail.
    """
    try:
        video = collection.get_video(video_id)
        thumbnail = video.generate_thumbnail()
        logging.info(f"Thumbnail generation successful. fn=thumbnail, video_id={video_id}")
        return thumbnail
    except Exception as e:
        logging.error(f"Thumbnail generation failed. fn=thumbnail, video_id={video_id}. error={e}")
        

def delete_video_from_index(collection: object, video_id: str) -> None:
    """
    Deletes a specific video from the index.

    Args:
        collection (object): The video collection object.
        video_id (str): The ID of the video to delete.
    """
    try:
        video = collection.get_video(video_id)
        video.delete()
        logging.info(f"Video deletion successful. fn=delete_video_from_index, video_id={video_id}")
    except Exception as e:
        logging.error(f"Video deletion failed. fn=delete_video_from_index, video_id={video_id}. error={e}")
        raise e



def delete_all_videos_from_index(collection: object) -> None:
    """
    Deletes all videos from the collection index.

    Args:
        collection (object): The video collection object.
    """
    try:
        for video in collection.get_videos():
            video.delete()
        logging.info(f"All videos deletion successful. fn=delete_all_videos_from_index")
    except Exception as e:
        logging.error(f"All videos deletion failed. fn=delete_all_videos_from_index. error={e}")


def show_collection(collection: object) -> List[object]:
    """
    Retrieves and returns a list of videos in the collection.

    Args:
        collection (object): The video collection object.

    Returns:
        List[object]: A list of videos in the collection.
    """
    try:
        videos_list = []
        for video in collection.get_videos():
            videos_list.append(video)
        logging.info(f"Collection list retrieval successful. fn=show_collection")
        return videos_list
    except Exception as e:
        logging.error(f"Collection list retrieval failed. fn=show_collection. error={e}")
        raise e


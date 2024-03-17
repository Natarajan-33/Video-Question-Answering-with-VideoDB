import os
from dotenv import load_dotenv
from videodb import connect, SearchType, play_stream

load_dotenv()

# Establish a connection to the video database
videodb_api_key = os.getenv("VIDEODB_KEY")
connection = connect(api_key=videodb_api_key)
collection = connection.get_collection()

def add_videos_to_index(youtube_urls):
    """Uploads videos to the database and indexes their spoken words."""
    for url in youtube_urls:
        try:
            collection.upload(url=url)
            print(f"Video: {url} uploaded successfully.")
            for video in collection.get_videos():
                video.index_spoken_words()
                print(f"Indexed spoken words in: {video.name}.")
        except Exception as error:
            print(f"Failed to upload and index {url}. Error: {error}")

def find_related_content_by_query(query):
    """Searches the database for content similar to the query and returns the first result."""
    try:
        search_results = collection.search(query=query)
        first_result = search_results.get_shots()[0]
        return first_result.text, {"video_title": first_result.video_title, "text": first_result.text}
    except Exception as error:
        print(f"Search failed for query '{query}'. Error: {error}")
        return "", {}
    

def stream_video(video_url):
    video = connection.upload(url=video_url)
    video.generate_stream()
    video.play()

def watch_shorts(video_url, topic):
    video = connection.upload(url=video_url)
    result = video.search(topic, search_type= SearchType.semantic)
    result.play()




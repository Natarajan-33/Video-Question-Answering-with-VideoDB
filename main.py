import streamlit as st
from db.database_operations import add_videos_to_index, chat_with_video, stream_video, watch_shorts, transcribe_video, add_subtitles, thumbnail, delete_video_from_index, delete_all_videos_from_index, show_collection
from llm.advanced_language_model import generate_answer_from_context
from utils.helpers import setup_logging
import logging

st.set_page_config(
    page_title="Video Insight Bot🤖", layout="wide", initial_sidebar_state="auto"
)


setup_logging('logs/videolens_logs.log')

# Load the CSS file
def load_css(css_file):
    try:
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        logging.info(f"CSS file '{css_file}' loaded successfully. fn= load_css")
    except Exception as e:
        logging.error(f"Error loading CSS file '{css_file}'. fn=load_css. Error: {e}")



# Call the function to load the styles
load_css("static/styles.css")

# Now render the text with the CSS class applied
st.sidebar.markdown(
    """
    <div class="bot-header">
        Video Insight Bot🤖
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

# Initialize session state variables if they don't exist
if 'video_urls' not in st.session_state:
    st.session_state.video_urls = []
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = ""
if 'urls_stored' not in st.session_state:
    st.session_state.urls_stored = False
if 'first_time' not in st.session_state:
    st.session_state.first_time = True
if 'video_dict' not in st.session_state:
    st.session_state.video_dict = None
if 'collection' not in st.session_state:
    st.session_state.collection = None
if 'collection_variables' not in st.session_state:
    st.session_state.collection_variables = False
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {}  # Stores chat histories for each video

def add_video_url():
    if st.session_state.video_url != "":
        st.session_state.video_urls.append(st.session_state.video_url)
        col1, _, _ = st.columns([2.5, 3, 2], gap="large")
        with col1:
            st.success(f"Video URL {st.session_state.video_url} added!")
        col1, _, _ = st.columns([3.5, 1, 2], gap="large")
        with col1:
            st.info("Feel free to include additional URLs by entering them below, or continue by clicking the 'Save the library to Database' button below.")
        logging.info(f"Video URL added: {st.session_state.video_url}")
        st.session_state.video_url = ""

def save_library():
    if st.session_state.collection_name != "":
        # Assuming add_videos_to_index is defined elsewhere
        st.session_state.video_dict, st.session_state.collection = add_videos_to_index(
            st.session_state.collection_name, st.session_state.video_urls)
        if st.session_state.video_dict is not None:
            st.session_state.urls_stored = True
            st.session_state.collection_variables = True
        else:
            col1, _, _ = st.columns([2.1, 3, 2], gap="large")
            with col1:
                st.error("Error uploading videos and indexing. Please try again.")
            st.session_state.urls_stored = False
    else:
        col1, _, _ = st.columns([2.1, 1, 2], gap="large")
        with col1:
            st.warning("Please provide the collection name and then click the 'Save the library to Database' button to continue.")

if not st.session_state.urls_stored:
    st.sidebar.write("Enter video collection name")
    st.sidebar.text_input("", placeholder="One collection name", label_visibility="collapsed", key="collection_name")
    st.subheader("Provide the YouTube Video URL")
    col1, col2, _ = st.columns([2.5, 3, 2])
    with col1:
        st.text_input("", placeholder="Paste here", label_visibility="collapsed", key="video_url")
    with col2:
        if st.button("Add video URL to library", on_click=add_video_url):
            pass
    st.divider()
    if st.button("Save the library to Database", on_click=save_library):
        pass

# st.divider()
st.sidebar.subheader("Select a Service:")
selected_service = st.sidebar.radio(
    "",
    ["***LLM Summary***", "***Stream Full Video***", "***Search and Watch Clip***", "***Get Transcript***", "***Add Subtitles***", "***Generate Thumbnail***","***Delete Video***", "***Delete All***"],
    captions=["Summarized Response", "Stream Video", "Watch Related Short Clips", "Video Transcript", "Watch with Subtitles", "Create Video Thumbnail","Delete the Video", "Delete All Videos"], label_visibility="collapsed")



if selected_service == "***LLM Summary***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()

    st.subheader("Select URL to chat with")
    video_name = st.selectbox(" ", st.session_state.video_dict.keys(), placeholder="Choose the video to stream",index=None, disabled=False, label_visibility="collapsed", key="chatbot")
    if video_name:
        if video_name not in st.session_state.chat_histories:
            st.session_state.chat_histories[video_name] = [{"role": "bot", "message": "Hello! Feel free to search through the video content. What's your question?"}] # Initialize chat history for the video if not exist
        
        for entry in st.session_state.chat_histories[video_name]:
            with st.chat_message(entry["role"]):
                st.write(entry["message"])


        query = st.chat_input("What would you like to know?")
        if query:
            st.session_state.chat_histories[video_name].append({"role": "user", "message": query})
            with st.chat_message("user"):
                st.write(query)

        if st.session_state.chat_histories[video_name][-1]["role"] != "bot":
            with st.chat_message("bot"):
                with st.spinner("Analyzing..."):
                    response_placeholder = st.empty()
                    search_context, details = chat_with_video(st.session_state.collection, st.session_state.video_dict[video_name], query)
                    response = ""
                    response = generate_answer_from_context(query, search_context)
                response_placeholder.write(response)

                st.session_state.chat_histories[video_name].append({"role": "bot", "message": response})

            with st.expander("Context and Details"):
                st.write(details)


if selected_service == "***Stream Full Video***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to stream it")
    video_name= st.selectbox(" ", st.session_state.video_dict.keys(), placeholder="Choose the video to stream",index=None, disabled=False, label_visibility="collapsed", key="stream")
    if video_name:
        with st.spinner("Streaming video in new tab..."):
            stream_video(st.session_state.collection, st.session_state.video_dict[video_name])


if selected_service == "***Search and Watch Clip***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to stream a clip from")
    video_name = st.selectbox(" ", st.session_state.video_dict.keys(), placeholder="Choose the video whose shorts you want to watch from", index=None, disabled=False, label_visibility="collapsed", key="shorts")
    if video_name:
        st.subheader("Enter the topic to get shorts relevant to that")
        topic = st.text_input(" ", placeholder="ask here")
        if topic:
            with st.spinner("Streaming shots in new tab..."):
                response = watch_shorts(st.session_state.collection, st.session_state.video_dict[video_name], topic)  
                if response.shots != []:
                    response.play()
                else:
                    st.info("No shorts matching the specified topic were found. Please try a different topic.")
                    

if selected_service == "***Get Transcript***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to get transcript from")
    video_name = st.selectbox(" ", st.session_state.video_dict.keys(), placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="transcript")
    if video_name:
        with st.spinner("Transcribing video..."):
            transcription = transcribe_video(st.session_state.collection, st.session_state.video_dict[video_name])  
            st.info(f"Transcript for {video_name} is:")
            st.success(transcription)


if selected_service == "***Add Subtitles***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to add subtitles to")
    video_name = st.selectbox(" ", st.session_state.video_dict.keys(), placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="subtitles")
    if video_name:
        with st.spinner("Adding subtitles to video and streaming video in new tab..."):
            transcription = add_subtitles(st.session_state.collection, st.session_state.video_dict[video_name])  


if selected_service == "***Generate Thumbnail***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to which you want to generate thumbnail for")
    video_name = st.selectbox(" ",st.session_state.video_dict.keys(), placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="thumbnail")
    if video_name:
        with st.spinner("Generating thumbnail..."):
            thumbnail_image = thumbnail(st.session_state.collection, st.session_state.video_dict[video_name])  
            st.image(thumbnail_image, width=300)


if selected_service == "***Delete Video***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL of the video which you want to delete")
    video_name = st.selectbox(" ", st.session_state.video_dict.keys(), index=None, placeholder="Choose an option", disabled=False, label_visibility="collapsed", key="delete_video")
    if video_name:
        with st.spinner("Deleting video..."):
            delete_video_from_index(st.session_state.collection, st.session_state.video_dict[video_name])  
            # st.session_state.video_urls.remove(video_link)
            if video_name in st.session_state.video_dict[video_name]:
                del st.session_state.video_dict[video_name]
            st.success("Video deleted successfully from the index.")


if selected_service == "***Delete All***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    if st.button("Click here to Delete All Videos"):
        with st.spinner("Deleting all videos..."):
            delete_all_videos_from_index(st.session_state.collection)  
            st.session_state.video_urls = []
            st.session_state.video_dict.clear()
            st.session_state.urls_stored = False
            st.session_state.chat_history = [
            {"role": "bot", "message": "Hello! Feel free to search through the video content. What's your question?"}
        ]
            col1, col2, col3 = st.columns([1.5,1,3], gap="large")
            with col1:
                st.success("All videos deleted successfully from the index.")

st.sidebar.divider()
if st.sidebar.button("Check collection") and st.session_state.collection_variables:
    video_list = show_collection(st.session_state.collection)
    st.divider()
    if video_list:
        st.subheader("Collection list:")
        st.write(video_list)
    else:
        col1, col2, col3 = st.columns([1.8,1,5], gap="large")
        with col1:
            st.info("No videos in the collection.")



# try playing shots videos




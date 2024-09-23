import streamlit as st
from db.database_operations import add_videos_to_index, chat_with_video, stream_video, watch_shorts, transcribe_video, add_subtitles, thumbnail, delete_video_from_index, delete_all_videos_from_index, show_collection
from llm.advanced_language_model import generate_answer_from_context


st.set_page_config(
    page_title="Video Insight Bot🤖", layout="wide", initial_sidebar_state="auto"
)

st.sidebar.title("Video Insight Bot🤖")
st.sidebar.divider()

def setup_session_variables():
    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = [
    #         {"role": "bot", "message": "Hello! Feel free to search through the video content. What's your question?"}
    #     ]
    if "video_urls" not in st.session_state:
        st.session_state.video_urls = []
    if "urls_stored" not in st.session_state:
        st.session_state.urls_stored = False
    if "first_time" not in st.session_state:
        st.session_state.first_time = True
    if "collection" not in st.session_state:
        st.session_state.collection = None
    if "collection_variables" not in st.session_state:
        st.session_state.collection_variables = False
    if "video_dict" not in st.session_state:
        st.session_state.video_dict = {}
    if 'chat_histories' not in st.session_state:
        st.session_state.chat_histories = {}  # Stores chat histories for each video


setup_session_variables()

if not st.session_state.urls_stored:
    st.sidebar.write("Enter video collection name")
    collection_name = st.sidebar.text_input("", placeholder="One collection name", label_visibility="collapsed")
    st.subheader("Provide the YouTube Video URL")
    video_url = st.text_input("", placeholder="Paste here", label_visibility="collapsed")
    if st.button("Add video URL to library"):
        st.session_state.video_urls.append(video_url)
        st.success(f"Video URL {video_url} added! ")
        st.info("Feel free to include additional URLs by entering them above, or continue by clicking the 'Save all video URLs to Database' button below.")
        video_url = ""

    if st.button("Save all video URLs to database"):
        if collection_name != "":
            with st.spinner("Uploading Videos and Indexing..."):
                st.session_state.video_dict, st.session_state.collection = add_videos_to_index(collection_name, st.session_state.video_urls)
                if st.session_state.video_dict != None:
                    st.success("Videos uploaded and indexed successfully!")
                    st.session_state.urls_stored = True
                    st.session_state.collection_variables = True
                else:
                    st.error("Error uploading videos and indexing. Please try again.")
                    st.session_state.urls_stored = False
        else:
            st.sidebar.warning("Please provide the collection name.")
elif st.session_state.first_time:
    col1, col2, col3 = st.columns([1.1,3,5], gap="large")
    with col1:
        st.success("Video URLs have been successfully saved.")
        st.session_state.first_time = False


# st.divider()
st.sidebar.subheader("Select a Service:")
selected_service = st.sidebar.radio(
    "",
    ["***LLM Summary***", "***Stream Full Video***", "***Search and Watch Clip***", "***Get Transcript***", "***Add Subtitles***", "***Generate Thumbnail***","***Delete Video***", "***Delete All***"],
    captions=["Summarized Response", "Stream Video", "Watch Related Short Clips", "Video Transcript", "Watch with Subtitles", "Create Video Thumbnail","Delete the Video", "Delete All Videos"], label_visibility="collapsed")



if selected_service == "***LLM Summary***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    # st.title("Video Insight Bot🤖")

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
            col1, col2, col3 = st.columns([1.1,3,5], gap="large")
            with col1:
                st.success("All videos deleted successfully from the index.")

st.sidebar.divider()
if st.sidebar.button("Check collection") and st.session_state.collection_variables:
    video_list = show_collection(st.session_state.collection)
    st.divider()
    st.write(video_list)





# metadata for video selection instead of URL
# try playing shots videos




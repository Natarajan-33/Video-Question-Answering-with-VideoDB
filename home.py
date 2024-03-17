import streamlit as st
from database_operations import add_videos_to_index, find_related_content_by_query, stream_video, watch_shorts, transcribe_video, add_subtitles, thumbnail, delete_video_from_index
from advanced_language_model import generate_answer_from_context


st.set_page_config(
    page_title="Video Insight Bot🤖", layout="wide", initial_sidebar_state="auto"
)

def setup_session_variables():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "message": "Hello! Feel free to search through the video content. What's your question?"}
        ]

    if "video_urls" not in st.session_state:
        st.session_state.video_urls = []

    if "urls_stored" not in st.session_state:
        st.session_state.urls_stored = False

setup_session_variables()

if not st.session_state.urls_stored:
    st.header("Provide the YouTube Video URL")
    video_url = st.text_input("", placeholder="Paste here", label_visibility="collapsed")
    if st.button("Add Video URL to Library"):
        st.session_state.video_urls.append(video_url)
        st.success(f"Video URL {video_url} added! Add more if you like.")
        video_url = ""

    if st.button("Save All Video URLs to Database"):
        st.session_state.urls_stored = True
        with st.spinner("Uploading Videos and Indexing..."):
            add_videos_to_index(st.session_state.video_urls)
            st.success("Videos uploaded and indexed successfully!")
else:
    st.success("Video URLs have been successfully saved.")

# st.divider()

selected_service = st.sidebar.radio(
    "Select a Service:",
    ["***LLM Summary***", "***Stream Full Video***", "***Search and Watch Clip***", "***Get Transcript***", "***Add Subtitles***", "***Generate Thumbnail***","***Delete Video***"],
    captions=["Summarized Response", "Stream Video", "Watch Related Short Clips", "Video Transcript", "Watch with Subtitles", "Create Video Thumbnail","Delete the Video"])



if selected_service == "***LLM Summary***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.title("Video Insight Bot🤖")

    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.write(entry["message"])

    query = st.chat_input("What would you like to know?")
    if query:
        st.session_state.chat_history.append({"role": "user", "message": query})
        with st.chat_message("user"):
            st.write(query)

    if st.session_state.chat_history[-1]["role"] != "bot":
        with st.chat_message("bot"):
            with st.spinner("Analyzing..."):
                response_placeholder = st.empty()
                search_context, details = find_related_content_by_query(query)
                response = ""
                response = generate_answer_from_context(query, search_context)
            response_placeholder.write(response)

            st.session_state.chat_history.append({"role": "bot", "message": response})

        with st.expander("Context and Details"):
            st.write(details)


if selected_service == "***Stream Full Video***" and st.session_state.urls_stored:
    st.header(selected_service)
    video_link = st.selectbox("Select URL to stream it", st.session_state.video_urls, placeholder="Choose an option", disabled=False, label_visibility="visible")
    if video_link:
        stream_video(video_url)


if selected_service == "***Search and Watch Clip***" and st.session_state.urls_stored:
    video_link = st.selectbox("Select URL to stream it", st.session_state.video_urls, placeholder="Choose an option", disabled=False, label_visibility="visible")
    topic = st.text_input("Enter the topic to get shorts relevant to that", placeholder="ask here", label_visibility="visible")
    if video_link:
        watch_shorts(video_url, topic)  




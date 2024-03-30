import streamlit as st
from database_operations import add_videos_to_index, find_related_content_by_query, stream_video, watch_shorts, transcribe_video, add_subtitles, thumbnail, delete_video_from_index, delete_all_videos_from_index
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
    if "first_time" not in st.session_state:
        st.session_state.first_time = True

setup_session_variables()

if not st.session_state.urls_stored:
    st.header("Provide the YouTube Video URL")
    video_url = st.text_input("", placeholder="Paste here", label_visibility="collapsed")
    if st.button("Add Video URL to Library"):
        st.session_state.video_urls.append(video_url)
        st.success(f"Video URL {video_url} added! ")
        st.info("Feel free to include additional URLs by entering them above, or continue by clicking the 'Save all video URLs to Database' button below.")
        video_url = ""

    if st.button("Save All Video URLs to Database"):
        st.session_state.urls_stored = True
        with st.spinner("Uploading Videos and Indexing..."):
            add_videos_to_index(st.session_state.video_urls)
            st.success("Videos uploaded and indexed successfully!")

elif st.session_state.first_time:
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
    st.divider()
    st.subheader("Select URL to stream it")
    video_link = st.selectbox(" ", st.session_state.video_urls, placeholder="Choose the video to stream",index=None, disabled=False, label_visibility="collapsed", key="stream")
    if video_link:
        with st.spinner("Streaming video in new tab..."):
            stream_video(video_link)


if selected_service == "***Search and Watch Clip***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to stream a clip from")
    video_link = st.selectbox(" ", st.session_state.video_urls, placeholder="Choose the video whose shorts you want to watch from", index=None, disabled=False, label_visibility="collapsed", key="shorts")
    if video_link:
        st.subheader("Enter the topic to get shorts relevant to that")
        topic = st.text_input(" ", placeholder="ask here")
        if topic:
            with st.spinner("Streaming shots in new tab..."):
                response = watch_shorts(video_link, topic)  
                if response.shots != []:
                    response.play()
                else:
                    st.info("No shorts matching the specified topic were found. Please try a different topic.")
                    

if selected_service == "***Get Transcript***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to get transcript from")
    video_link = st.selectbox(" ", st.session_state.video_urls, placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="transcript")
    if video_link:
        with st.spinner("Transcribing video..."):
            transcription = transcribe_video(video_link)  
            st.info(f"Transcript for {video_link} is:")
            st.success(transcription)


if selected_service == "***Add Subtitles***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to add subtitles to")
    video_link = st.selectbox(" ", st.session_state.video_urls, placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="subtitles")
    if video_link:
        with st.spinner("Adding subtitles to video and streaming video in new tab..."):
            transcription = add_subtitles(video_link)  


if selected_service == "***Generate Thumbnail***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to which you want to generate thumbnail for")
    video_link = st.selectbox(" ", st.session_state.video_urls, placeholder="Choose an option", index=None, disabled=False, label_visibility="collapsed", key="thumbnail")
    if video_link:
        with st.spinner("Generating thumbnail..."):
            thumbnail_image = thumbnail(video_link)  
            st.image(thumbnail_image, width=300)


if selected_service == "***Delete Video***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    st.subheader("Select URL to which you want to generate thumbnail for")
    video_link = st.selectbox(" ", st.session_state.video_urls, index=None, placeholder="Choose an option", disabled=False, label_visibility="collapsed", key="delete_video")
    if video_link:
        with st.spinner("Deleting video..."):
            delete_video_from_index(video_link)  
            st.session_state.video_urls.remove(video_link)
            st.success("Video deleted successfully from the index.")


if selected_service == "***Delete All***" and st.session_state.urls_stored:
    st.header(selected_service)
    st.divider()
    if st.button("Click here to Delete All Videos"):
        with st.spinner("Deleting all videos..."):
            delete_all_videos_from_index()  
            st.session_state.video_urls = []
            st.session_state.urls_stored = False
            st.session_state.chat_history = [
            {"role": "bot", "message": "Hello! Feel free to search through the video content. What's your question?"}
        ]
            st.success("All videos deleted successfully from the index.")



# metadata for video selection instead of URL
# try playing shots videos
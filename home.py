import streamlit as st
from db_utils import upload_videos_to_database, getanswer

st.set_page_config(
    page_title="Youtube Video Query Bot🤖", layout="wide", initial_sidebar_state="auto"
)

def initialize_session_state():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! Now, you can query over provided video contents. Shot the questions"}
        ]

    if "youtube_links" not in st.session_state.keys():
        st.session_state.youtube_links = []

    if "links_submitted" not in st.session_state.keys():
        st.session_state.links_submitted = False

initialize_session_state()

st.header("Enter the YouTube Video Link")
if not st.session_state.links_submitted:
    youtube_link = st.text_input("",placeholder= "Enter here" ,  label_visibility="collapsed")
    if st.button("Add youTube link to collection"):
        st.session_state.youtube_links.append(youtube_link)
        st.success(f"YouTube link {youtube_link} added successfully!")
        youtube_link = ""

    if st.button("Submit all youTube links to database engine"):
        st.session_state.links_submitted = True
        with st.spinner("Uploading and Indexing Video"):
            upload_videos_to_database(st.session_state.youtube_links)
            st.success("All youtube links has uploaded and indexed successfully!")
else:
    st.success("The provided youtube links has been submitted and stored.")

st.divider()
if st.session_state.links_submitted:
    st.title("Youtube Video Query Bot🤖")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_query := st.chat_input("Enter query"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking🤔"):
                res_box = st.empty()
                final_response, matching_videos = getanswer(user_query)
            res_box.write(f"{final_response}")

            st.session_state.messages.append({"role": "assistant", "content": final_response})

        with st.expander(f"Context Details"):
                st.write(matching_videos)

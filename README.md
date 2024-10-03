# VideoLens: Video Insight Bot Application

![VideoLens App](https://github.com/user-attachments/assets/e09ce790-b7bb-493a-b741-14f77f3c78a1)

## Table of Contents

- [Introduction](#introduction)
  - [Key Features](#key-features)
  - [Streamlit UI](#streamlit-ui)
- [Installation](#installation)
- [Tools and Technologies](#tools-and-technologies)
- [Troubleshooting](#troubleshooting)
  - [1. Errors During Video Processing](#1-errors-during-video-processing)
  - [2. Streamlit Application Issues](#2-streamlit-application-issues)
- [Contributing](#contributing)

## Introduction

VideoLens is a robust and versatile Video Insight Bot application designed to provide users with an interactive way to engage with YouTube videos. By combining powerful tools and technologies—such as video indexing, Large Language Models (LLMs), and a Streamlit UI—VideoLens offers an intuitive interface for extracting valuable insights from your video collections.

### Key Features

- **Video Collection Management:** Easily add YouTube video URLs to your personal collection for analysis and interaction.
- **LLM Summary and Chatbot Interaction:** Engage with video content through a chatbot interface, asking questions and receiving summarized responses based on the video's content.
- **Stream Full Videos and Clips:** Stream full videos directly within the app or search for specific topics within videos to watch relevant clips.
- **Transcript Generation:** Obtain the transcript of any video in your collection.
- **Subtitles and Thumbnail Generation:** Add subtitles to videos for better accessibility and generate custom thumbnails.
- **Video Deletion:** Delete individual videos or clear your entire video collection as needed.

### Streamlit UI

VideoLens comes equipped with a Streamlit-based user interface, ensuring a user-friendly experience while interacting with the application. The streamlined design facilitates easy navigation and efficient utilization of the application's capabilities, including:

- **Adding and Managing Video URLs:** Input YouTube video URLs to build your collection.
- **Selecting Services:** Choose from a range of services like **LLM Summary, Stream Video, Search and Watch Clip, Get Transcript, Add Subtitles, Generate Thumbnail, and Delete Videos**.
- **Chatbot Interaction:** Engage in conversations with the chatbot, view conversation history, and access retrieved transcripts and videos through expandable sections.

## Installation

To get started with VideoLens, follow these steps:

```bash
# Clone the repository
git clone https://github.com/YourUsername/VideoLens.git
cd VideoLens

# Create a virtual environment (recommended)
python -m venv videolens_env

# Activate the virtual environment
# On Windows:
videolens_env\Scripts\activate
# On macOS/Linux:
source videolens_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run main.py
```

## Tools and Technologies

VideoLens harnesses the power of several cutting-edge tools and technologies:

- **Video Database (VideoDB):** Efficiently stores and indexes video data for quick retrieval and processing.
- **Large Language Models (LLMs):** Utilizes advanced language models to generate answers from video content, enabling interactive chatbot experiences.
- **YouTube Video Processing:**
  - **Transcription:** Extracts transcripts from YouTube videos for analysis.
  - **Subtitles:** Adds subtitles to videos for enhanced accessibility.
  - **Thumbnail Generation:** Creates custom thumbnails for videos.
- **Streamlit UI:** Provides an intuitive and visually appealing frontend for an enhanced user experience.

<!-- ## Troubleshooting

### 1. Errors During Video Processing

If you experience errors while processing videos (e.g., streaming, transcribing, generating thumbnails), it might be due to issues with external libraries or APIs.

**Possible Causes:**

- Invalid or inaccessible YouTube URLs.
- Network connectivity issues.
- Missing or outdated dependencies.

**Solutions:**

- **Verify YouTube URLs:** Ensure that the video URLs you provide are valid and accessible.
- **Check Internet Connection:** Confirm that you have a stable internet connection.
- **Update Dependencies:** Run `pip install --upgrade -r requirements.txt` to update all dependencies.

### 2. Streamlit Application Issues

If the Streamlit application fails to run or you encounter UI-related issues:

**Possible Causes:**

- Streamlit is not properly installed.
- Conflicts with other packages in your environment.

**Solutions:**

- **Reinstall Streamlit:**
  ```bash
  pip uninstall streamlit
  pip install streamlit
  ```
- **Check for Conflicting Packages:** Ensure that there are no package conflicts in your virtual environment.
- **Use the Correct Command to Run the App:**
  ```bash
  streamlit run main.py
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes. -->

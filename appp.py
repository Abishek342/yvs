import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# Title for the Streamlit App
st.title("YouTube Video Summarizer")
st.write("Enter a YouTube video link to get its summarized transcript.")

# Input for the YouTube video link
youtube_video = st.text_input("YouTube Video URL", "")

# Define function to extract the video ID
def extract_video_id(youtube_video):
    if "watch?v=" in youtube_video:
        return youtube_video.split("watch?v=")[1].split("&")[0]
    elif "youtu.be" in youtube_video:
        return youtube_video.split("/")[-1].split("?")[0]
    else:
        return None

# Check if the user has provided the YouTube video link
if youtube_video:
    video_id = extract_video_id(youtube_video)
    
    if video_id:
        st.write("Extracting transcript...")

        try:
            # Get the transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            # Combine all transcript texts into one string
            result = ""
            for i in transcript:
                result += ' ' + i['text']
            st.write(f"Transcript length: {len(result)} characters")

            # Summarizer pipeline
            summarizer = pipeline('summarization')

            # Split into chunks of 1000 characters and summarize
            num_iters = int(len(result) / 1000)
            summarized_text = []

            for i in range(0, num_iters + 1):
                start = i * 1000
                end = (i + 1) * 1000
                input_text = result[start:end]
                
                if input_text:
                    st.write(f"Input text chunk {i+1}:\n", input_text)
                    out = summarizer(input_text)
                    out = out[0]['summary_text']
                    st.write(f"Summarized text chunk {i+1}:\n", out)
                    summarized_text.append(out)

            # Join summarized text
            final_summary = " ".join(summarized_text)
            st.subheader("Final Summarized Transcript:")
            st.write(final_summary)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    else:
        st.error("Invalid YouTube URL format. Please check the link.")

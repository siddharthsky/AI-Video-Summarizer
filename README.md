<h1 align="center">
  <br>
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer"><img src="https://i.imgur.com/Jk1wxO3.png" alt="AI YouTube Video Summarizer" width="200"></a>
  <br>
   🎥 AI Video Summarization & Timestamp Generator
  <br>
</h1>

<h4 align="center">Harnessing the Power of LLMs for Enhanced Video Understanding</h4>

<p align="center">
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/issues"><img src="https://img.shields.io/github/issues/siddharthsky/google-gemini-yt-video-summarizer-AI-p"></a> 
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/stargazers"><img src="https://img.shields.io/github/stars/siddharthsky/google-gemini-yt-video-summarizer-AI-p"></a>
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
</p>

<p align="center">
  <a href="#overview-">Overview</a> •
  <a href="#features-">Features</a> •
  <a href="#getting-started-">Getting Started</a> •
  <a href="#contributing">Contributing</a> 
</p>

<p align="center">
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer"><img src="https://github.com/siddharthsky/AI-Video-Summarizer/blob/main/research/demo4.gif" alt="Usage Demo"></a>
</p>




## Overview 📝

This project is an AI-powered video summarizer designed specifically for YouTube videos. Leveraging the Google Gemini API, it employs advanced machine learning techniques to analyze and condense lengthy YouTube videos into concise summaries, providing users with quick insights into the video content.


## Features ✨

- Automatic extraction of key insights and timestamps from YouTube videos.
- Utilizes youtube-transcript-api for getting the transcripts/subtitles YouTube video.
- Option for users to select AI models like *GPT* or *Gemini* for summarization.
- Efficiently summarizes videos, reducing viewing time while preserving essential information.

## Getting Started 🚀

### Prerequisites

- Python 3.10
- LLM Model API Keys [[🔑]](https://github.com/siddharthsky/AI-Video-Summarizer/tree/main?tab=readme-ov-file#get-api-keys)

### Usage

1. Clone the repository:
```
git clone https://github.com/siddharthsky/AI-Video-Summarizer.git
```
2. Navigate to the project directory:
```
cd AI-Video-Summarizer
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Create a ".env" file ⬇️ [add whichever is available]
```
GOOGLE_GEMINI_API_KEY = "Your-Gemini-Key-Here"
OPENAI_API_KEY = "Your-Openai-Key-Here"
```

### Get API Keys:

- [Google Gemini API key](https://makersuite.google.com/app/apikey) 🔑 
   
- [OpenAI API key](https://platform.openai.com/signup) 🔑 
   

5 Run the summarizer:
```
streamlit run app.py
```


## Contributing

Contributions are welcome from the community!, Whether it's feedback, suggestions, or code improvements, your input is valuable. 

## Acknowledgments

- [Google Gemini](https://ai.google.dev/)
- [OpenAI GPT](https://help.openai.com/en/) 
- [Krish Naik](https://www.youtube.com/user/krishnaik06) 

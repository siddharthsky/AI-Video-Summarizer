import streamlit as st
import os
from dotenv import load_dotenv
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from src.misc import Misc
from src.timestamp_formatter import TimestampFormatter
from src.copy_module_edit import ModuleEditor
from st_copy_to_clipboard import st_copy_to_clipboard

@st.cache_data(show_spinner=False)
def get_transcript_cached(url):
    try:
        return GetVideo.transcript(url)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def get_transcript_time_cached(url):
    try:
        return GetVideo.transcript_time(url)
    except Exception:
        return None

class AIVideoSummarizer:

    def __init__(self):
        load_dotenv()

        self.youtube_url = None
        self.video_id = None
        self.video_title = None
        self.video_transcript = None
        self.video_transcript_time = None
        self.summary = None
        self.time_stamps = None
        self.transcript = None

        self.model_name = None
        self.gemini_model_type = "gemini-2.5-flash"
        self.openai_model_type = "gpt-5-nano"

        self.model_env_checker = []

    def header(self):

        st.markdown("""
        <style>

        .main-title{
            text-align:center;
            font-size:40px;
            font-weight:700;
            margin-bottom:10px;
        }

        .sub-title{
            text-align:center;
            font-size:18px;
            opacity:0.7;
            margin-bottom:30px;
        }

        .card{
            padding:20px;
            border-radius:12px;
            border:1px solid rgba(255,255,255,0.1);
            background:rgba(255,255,255,0.02);
        }

        .video-title{
            font-size:22px;
            font-weight:600;
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="main-title">🎬 AI Video Summarizer</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">Generate AI summaries, timestamps, and transcripts from YouTube videos</div>', unsafe_allow_html=True)


    def get_youtube_info(self):

        with st.container():

            st.markdown("### 🔗 YouTube Video")

            self.youtube_url = st.text_input(
                "Paste video link",
                placeholder="https://youtube.com/watch?v=..."
            )

        if os.getenv("GOOGLE_GEMINI_API_KEY"):
            self.model_env_checker.append("Gemini")

        if os.getenv("OPENAI_API_KEY"):
            self.model_env_checker.append("OpenAI")

        if not self.model_env_checker:
            st.warning("No API keys detected", icon="⚠️")


        st.markdown("### 🤖 AI Model")

        self.model_name = st.selectbox(
            "Select Model",
            self.model_env_checker
        )

        if self.model_name == "Gemini":

            gemini_models = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3-flash-preview",
                "Custom"
            ]

            selected_model = st.selectbox(
                "Gemini Model",
                gemini_models
            )

            if selected_model == "Custom":

                self.gemini_model_type = st.text_input(
                    "Enter Gemini model name",
                    placeholder="ex: gemini-2.5-pro"
                )

            else:
                self.gemini_model_type = selected_model

        if self.model_name == "OpenAI":

            openai_models = [
                "gpt-5-nano",
                "gpt-5-mini",
                "gpt-4.1",
                "gpt-4.1-mini",
                "gpt-4.1-nano",
                "Custom"
            ]

            selected_model = st.selectbox(
                "OpenAI Model",
                openai_models
            )

            if selected_model == "Custom":

                self.openai_model_type = st.text_input(
                    "Enter OpenAI model name",
                    placeholder="ex: gpt-4o-mini or gpt-5"
                )

            else:
                self.openai_model_type = selected_model

        if self.model_name == "OpenAI" and not self.openai_model_type:
            st.warning("Please enter an OpenAI model name")
            st.stop()

        if self.model_name == "Gemini" and not self.gemini_model_type:
            st.warning("Please enter a Gemini model name")
            st.stop()


        if self.youtube_url:

            self.video_id = GetVideo.Id(self.youtube_url)

            if self.video_id is None:
                st.error("Invalid YouTube link")
                st.stop()

            self.video_title = GetVideo.title(self.youtube_url)

            st.divider()

            st.markdown(
                f'<div class="video-title">{self.video_title}</div>',
                unsafe_allow_html=True
            )


            st.video(self.youtube_url)

            # st.image(
            #     f"https://img.youtube.com/vi/{self.video_id}/maxresdefault.jpg",
            #     use_container_width=True
            # )



    def generate_summary(self, loader):

        if st.button("✨ Generate Summary", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader, expanded=True) as status:

                status.update(label="Fetching transcript...", state="running")

                self.video_transcript = get_transcript_cached(self.youtube_url)

                status.update(label="Generating AI summary...", state="running")

                if self.model_name == "Gemini":

                    self.summary = Model.google_gemini(
                        transcript=self.video_transcript,
                        prompt=Prompt.prompt1(),
                        model_type=self.gemini_model_type
                    )

                else:

                    self.summary = Model.openai_gpt(
                        transcript=self.video_transcript,
                        prompt=Prompt.prompt1(),
                        model_type=self.openai_model_type
                    )

                status.update(label="Summary generated!", state="complete")

            st.markdown("## 📄 Summary")

            st.write(self.summary)

            col1, col2 = st.columns(2)

            with col1:
                st_copy_to_clipboard(self.summary)

            with col2:
                st.download_button(
                    "Download",
                    self.summary,
                    file_name=f"{self.video_title}_summary.txt"
                )



    def generate_time_stamps(self, loader):

        if st.button("⏱ Generate Timestamps", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader, expanded=True) as status:

                status.update(label="Fetching transcript...", state="running")
                
                self.video_transcript_time = get_transcript_time_cached(self.youtube_url)

                status.update(label="Generating timestamps...", state="running")

                youtube_url_full = f"https://youtube.com/watch?v={self.video_id}"

                if self.model_name == "Gemini":

                    self.time_stamps = Model.google_gemini(
                        self.video_transcript_time,
                        Prompt.prompt1(ID='timestamp'),
                        extra=youtube_url_full,
                        model_type=self.gemini_model_type
                    )

                else:

                    self.time_stamps = Model.openai_gpt(
                        self.video_transcript_time,
                        Prompt.prompt1(ID='timestamp'),
                        extra=youtube_url_full,
                        model_type=self.openai_model_type
                    )


            st.markdown("## ⏰ Timestamps")

            st.markdown(self.time_stamps)

            cp_text = TimestampFormatter.format(self.time_stamps)

            col1, col2 = st.columns(2)

            with col1:
                st_copy_to_clipboard(cp_text)

            with col2:
                st.download_button(
                    "Download",
                    cp_text,
                    file_name=f"{self.video_title}_timestamps.txt"
                )



    def generate_transcript(self, loader):

        if st.button("📜 Get Transcript", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader, expanded=True) as status:

                status.update(label="Fetching transcript...", state="running")

                self.video_transcript = get_transcript_cached(self.youtube_url)
                self.transcript = self.video_transcript

                status.update(label="Transcript ready!", state="complete")

            st.markdown("## Transcript")

            st.download_button(
                "Download Transcript",
                self.transcript,
                file_name=f"{self.video_title}_transcript.txt"
            )

            st.text_area(
                "Transcript",
                self.transcript,
                height=400
            )

            st_copy_to_clipboard(self.transcript)

    def validate_inputs(self):

        if not self.youtube_url:
            st.warning("Please paste a YouTube URL first.", icon="⚠️")
            return False

        if not self.video_id:
            st.error("Invalid YouTube URL.")
            return False

        if not self.model_name:
            st.warning("Please select an AI model.", icon="⚠️")
            return False

        return True


    def run(self):

        st.set_page_config(
            page_title="AI Video Summarizer",
            page_icon="🎬",
            layout="wide"
        )

        editor = ModuleEditor('st_copy_to_clipboard')
        editor.modify_frontend_files()

        ran_loader = Misc.loaderx()
        n, loader = ran_loader[0], ran_loader[1]    

        self.header()

        left, right = st.columns([1, 1.2], gap="large")

        with left:
            self.get_youtube_info()

        with right:

            st.markdown("### ⚡ Generate")

            mode = st.radio(
                "Select Output",
                  [":rainbow[**AI Summary**]", ":rainbow[**AI Timestamps**]", "**Transcript**"],
                horizontal=True
            )

            st.divider()

            if mode == ":rainbow[**AI Summary**]":
                self.generate_summary(loader[n])

            elif mode == ":rainbow[**AI Timestamps**]":
                self.generate_time_stamps(loader[n])

            else:
                self.generate_transcript(loader[0])

        st.divider()

        st.write(Misc.footer(), unsafe_allow_html=True)


if __name__ == "__main__":
    app = AIVideoSummarizer()
    app.run()
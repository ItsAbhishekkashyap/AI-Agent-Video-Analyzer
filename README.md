# 🎬 AI Video Analyzer

AI Video Analyzer is an intelligent meeting and video assistant that automates the transcription, summarization, and extraction of key insights from YouTube videos or local audio/video files. It also provides an interactive RAG (Retrieval-Augmented Generation) chat interface, allowing you to ask questions directly to your video's content!

## 🚀 Features

- **YouTube & Local File Support**: Download and extract audio directly from YouTube URLs, or supply your own local media files (`.mp4`, `.mp3`, `.wav`, etc.).
- **Local Transcription**: Uses OpenAI's Whisper model locally to quickly and accurately transcribe audio without needing a paid API.
- **Intelligent Summarization**: Leverages Mistral via LangChain to generate accurate meeting titles and concise summaries.
- **Insight Extraction**: Automatically identifies and groups **Action Items**, **Key Decisions**, and **Open Questions** from your videos.
- **RAG Chat Interface**: Uses ChromaDB and HuggingFace Embeddings to let you chat with your transcript in real-time.
- **Beautiful Streamlit UI**: A clean, modern, tab-based web interface to view your results.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**: Web Interface
- **OpenAI Whisper**: Speech-to-Text Transcription
- **LangChain & Mistral**: LLM Orchestration and Summarization
- **ChromaDB**: Local Vector Store for RAG
- **HuggingFace Sentence Transformers**: Local Embeddings
- **yt-dlp & FFmpeg**: Audio downloading and processing

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd AI-Video-Assistant-
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv

   # Windows
   .venv\\Scripts\\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r Requirements.txt
   ```

4. **Install FFmpeg (Required for audio processing):**
   - **Windows:** Install via `winget install ffmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to your PATH.
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`

## 🔑 Configuration

Create a `.env` file in the root directory and add your required API keys:

```ini
MISTRAL_API_KEY="your_mistral_api_key_here"
# Add any other required API keys here (e.g. TAVILY_API_KEY, SARVAM_API_KEY, etc.)
```

## 💻 Usage

### Streamlit Web Interface (Recommended)

Run the following command to launch the beautiful web UI:

```bash
streamlit run app.py
```

This will open a new tab in your web browser where you can input URLs, view the tabs containing action items, and chat with the RAG engine.

### CLI Interface

If you prefer using the terminal, you can run the main pipeline script:

```bash
python main.py
```

You will be prompted to enter a YouTube URL or file path, and the parsed output (along with the chat interface) will run directly in your command line.

## 📁 Project Structure

```
AI-Video-Assistant-/
│
├── core/
│   ├── transcriber.py     # Whisper audio transcription
│   ├── summarizer.py      # Mistral integration for summaries
│   ├── extractor.py       # Key decision and action item extraction
│   └── rag_engine.py      # ChromaDB and LangChain chat logic
│
├── utils/
│   └── audio_processor.py # yt-dlp & FFmpeg handling
│
├── app.py                 # Streamlit UI
├── main.py                # Command-Line Interface
├── Requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have ideas for improvements.

## 📝 License

This project is licensed under the MIT License.

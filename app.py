import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom minimal styling to make it feel premium without breaking native components
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 75, 43, 0.1);
        border-bottom: 2px solid #FF4B2B;
    }
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.markdown("### 🎬 AI Video Analyzer")
    st.caption("Turn any video or meeting into actionable insights in seconds.")
    st.divider()
    
    st.subheader("Input Source")
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=...")
    language = st.selectbox("Language", ["English", "Hinglish"], index=0).lower()
    
    analyze_btn = st.button("🚀 Analyze Video", use_container_width=True, type="primary")
    
    if st.session_state.result:
        st.divider()
        st.success("✅ Analysis Complete")
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

st.markdown('<p class="main-title">AI Video Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Transcribe, Summarize, and Chat with your video content instantly.</p>', unsafe_allow_html=True)

if analyze_btn:
    if not source.strip():
        st.sidebar.error("Please enter a valid URL or path.")
    else:
        st.session_state.result = None
        st.session_state.chat_history = []
        
        with st.status("Analyzing video... this may take a few minutes.", expanded=True) as status:
            try:
                st.write("🎵 Downloading & Processing Audio...")
                chunks = process_input(source)
                
                st.write("📝 Transcribing Audio...")
                transcript = transcribe_all(chunks, language)
                
                st.write("🧠 Generating Summary & Title...")
                title = generate_title(transcript)
                summary = summarize(transcript)
                
                st.write("🎯 Extracting Insights...")
                action_items = extract_action_items(transcript)
                decisions = extract_key_decisions(transcript)
                questions = extract_questions(transcript)
                
                st.write("📚 Building RAG Database for Chat...")
                rag_chain = build_rag_chain(transcript)
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                st.session_state.result = {
                    "title": title,
                    "transcript": transcript,
                    "summary": summary,
                    "action_items": action_items,
                    "key_decisions": decisions,
                    "open_questions": questions,
                    "rag_chain": rag_chain,
                }
                st.rerun()
                
            except Exception as e:
                status.update(label="An error occurred during analysis.", state="error", expanded=True)
                st.error(str(e))

if st.session_state.result:
    res = st.session_state.result
    
    st.markdown(f"## 📌 {res['title']}")
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Insights", "💬 Chat", "📝 Full Transcript"])
    
    with tab1:
        st.subheader("Executive Summary")
        st.info(res['summary'])
        
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("✅ Action Items")
            st.success(res['action_items'])
        with col2:
            st.subheader("🔑 Key Decisions")
            st.warning(res['key_decisions'])
            
        st.divider()
        st.subheader("❓ Open Questions")
        st.info(res['open_questions'])
        
    with tab3:
        st.subheader("💬 Chat with your Video")
        st.caption("Ask questions about the content of the video, and the AI will answer based on the transcript.")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat input
        if prompt := st.chat_input("Ask a question about this video..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_question(res["rag_chain"], prompt)
                st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
    with tab4:
        st.subheader("Transcript")
        with st.container(height=500):
            st.text(res['transcript'])
else:
    if not analyze_btn:
        st.info("👈 Enter a YouTube URL or Video File Path in the sidebar to get started.")
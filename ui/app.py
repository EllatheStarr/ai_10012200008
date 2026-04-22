"""
File: app.py
Author: Emmanuella Uwudia
Index Number: AI_10012200008
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Streamlit UI for Brew & Ask - Warm Coffee Shop Theme (Mobile Responsive)
"""

import streamlit as st
import sys
import os
import re

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import GhanaRAGPipeline
from src.innovation_feedback import GhanaFeedbackLoop

# ============================================
# CHECK AND REBUILD VECTOR INDEX IF MISSING
# ============================================
def check_and_rebuild_index():
    """Check if vector index files exist, rebuild if missing."""
    index_path = "data/vectors/faiss_index.bin"
    metadata_path = "data/vectors/chunk_metadata.json"
    
    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        st.warning("🔨 Vector index not found. Building it now (this may take 2-3 minutes)...")
        
        with st.status("Building vector index for cloud deployment...", expanded=True) as status:
            status.update(label="Step 1/4: Cleaning and processing data...")
            import subprocess
            subprocess.run(["python", "src/data_cleaning.py"], capture_output=True)
            
            status.update(label="Step 2/4: Creating chunks...")
            subprocess.run(["python", "src/chunking.py"], capture_output=True)
            
            status.update(label="Step 3/4: Generating embeddings...")
            subprocess.run(["python", "src/embeddings.py"], capture_output=True)
            
            status.update(label="Step 4/4: Building FAISS index...")
            subprocess.run(["python", "src/vector_store.py"], capture_output=True)
            
            status.update(label="✅ Index built successfully!", state="complete")
        
        st.success("✅ Vector index is ready! You can now ask questions.")
        return True
    return False

# Run the check before initializing the app
check_and_rebuild_index()
# ============================================

# Page configuration
st.set_page_config(
    page_title="Brew & Ask - Your Friendly Assistant",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Warm Coffee Shop Colors
CREAM = "#FFF8E7"
COFFEE_BROWN = "#6F4E37"
LATTE = "#C4A484"
TERRACOTTA = "#E2725B"
HONEY = "#F0A500"
DARK_BROWN = "#3E2723"
WHITE = "#FFFFFF"

# Custom CSS for Coffee Shop Theme with Mobile Responsive Fixes
st.markdown(
    f"""
    <style>
    .main {{
        background-color: {CREAM};
    }}
    
    .stApp {{
        background-color: {CREAM};
    }}
    
    .coffee-header {{
        background: linear-gradient(135deg, {COFFEE_BROWN} 0%, {DARK_BROWN} 100%);
        padding: 1.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border: 1px solid {LATTE};
    }}
    
    .coffee-header h1 {{
        color: {HONEY};
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }}
    
    .coffee-header p {{
        color: {LATTE};
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    }}
    
    .user-message {{
        background: linear-gradient(135deg, {TERRACOTTA} 0%, {HONEY} 100%);
        color: {WHITE};
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-weight: 500;
    }}
    
    .bot-message {{
        background-color: {WHITE};
        color: {DARK_BROWN};
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 75%;
        float: left;
        clear: both;
        border: 1px solid {LATTE};
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        line-height: 1.5;
    }}
    
    .source-card {{
        background-color: {WHITE};
        border-left: 4px solid {TERRACOTTA};
        padding: 12px;
        margin: 10px 0;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        font-size: 0.85rem;
    }}
    
    .score-high {{ 
        background-color: #D4E6D4;
        color: #2E7D32;
        padding: 2px 8px;
        border-radius: 20px;
        font-weight: bold;
    }}
    
    .score-medium {{ 
        background-color: #FFF3E0;
        color: #E65100;
        padding: 2px 8px;
        border-radius: 20px;
        font-weight: bold;
    }}
    
    .score-low {{ 
        background-color: #FFEBEE;
        color: #CE1126;
        padding: 2px 8px;
        border-radius: 20px;
        font-weight: bold;
    }}
    
    .stButton > button {{
        background-color: {COFFEE_BROWN};
        color: {WHITE};
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .stButton > button:hover {{
        background-color: {TERRACOTTA};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    .stButton button[key="view_stats"] {{
        background-color: {COFFEE_BROWN} !important;
        color: {WHITE} !important;
        border: 2px solid {HONEY} !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        padding: 0.6rem 1.2rem !important;
        width: 100% !important;
    }}
    
    .stButton button[key="view_stats"]:hover {{
        background-color: {TERRACOTTA} !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {COFFEE_BROWN};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {CREAM};
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: {CREAM} !important;
        opacity: 1 !important;
    }}

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: {WHITE} !important;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
    }}

    [data-testid="stSidebar"] button {{
        background-color: {COFFEE_BROWN} !important;
        color: {WHITE} !important;
        border: 3px solid {HONEY} !important;
        outline: 2px solid rgba(255, 248, 231, 0.65) !important;
        outline-offset: 1px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        width: 100% !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
    }}

    [data-testid="stSidebar"] button:hover {{
        background-color: {TERRACOTTA} !important;
        border-color: {HONEY} !important;
    }}

    /* Keep the View Statistics button outlined on all screen sizes */
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {{
        border: 3px solid {HONEY} !important;
        outline: 2px solid {HONEY} !important;
        outline-offset: 2px !important;
        border-radius: 12px !important;
        background-color: {COFFEE_BROWN} !important;
        color: {WHITE} !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.22) !important;
    }}

    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {{
        border: 3px solid {HONEY} !important;
        outline: 2px solid {HONEY} !important;
        outline-offset: 2px !important;
        border-radius: 12px !important;
        background-color: {COFFEE_BROWN} !important;
        color: {WHITE} !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.22) !important;
    }}

    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {{
        background-color: {TERRACOTTA} !important;
        border-color: {HONEY} !important;
        outline-color: {HONEY} !important;
    }}
    
    [data-testid="stSidebar"] .stAlert {{
        background-color: {DARK_BROWN};
        border-left-color: {HONEY};
    }}
    
    .stTextInput input {{
        background-color: {WHITE};
        color: {DARK_BROWN};
        border: 2px solid {LATTE};
        border-radius: 30px;
        padding: 12px 20px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput input:focus {{
        border-color: {TERRACOTTA};
        box-shadow: 0 0 0 3px rgba(226,114,91,0.2);
        outline: none;
    }}
    
    [data-testid="stSlider"] {{
        color: {HONEY};
    }}
    
    .stCheckbox label {{
        color: {CREAM};
    }}
    
    .stAlert {{
        background-color: {DARK_BROWN};
        border-left-color: {HONEY};
        color: {CREAM};
        border-radius: 12px;
    }}
    
    h1, h2, h3, h4 {{
        color: {COFFEE_BROWN};
        font-weight: 600;
    }}
    
    hr {{
        border-color: {LATTE};
        margin: 20px 0;
    }}
    
    .stats-container {{
        background-color: {WHITE};
        border: 2px solid {COFFEE_BROWN};
        border-radius: 16px;
        padding: 15px;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .stats-title {{
        color: {COFFEE_BROWN};
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
        text-align: center;
    }}

    .memory-status {{
        background-color: {WHITE};
        color: {DARK_BROWN};
        border-left: 5px solid {HONEY};
        border-radius: 12px;
        padding: 12px 14px;
        margin-top: 8px;
        font-weight: 700;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
    }}

    .memory-status strong {{
        color: {COFFEE_BROWN};
    }}
    
    .stats-metric {{
        background-color: {CREAM};
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        margin: 5px 0;
    }}
    
    .stats-number {{
        font-size: 1.8rem;
        font-weight: bold;
        color: {TERRACOTTA};
    }}
    
    .stats-label {{
        font-size: 0.8rem;
        color: {DARK_BROWN};
    }}
    
    .rating-bar {{
        background-color: {CREAM};
        border-radius: 10px;
        padding: 8px;
        margin: 5px 0;
    }}
    
    @media (max-width: 768px) {{
        .coffee-header {{
            padding: 0.8rem !important;
            margin-bottom: 1rem !important;
        }}
        
        .coffee-header h1 {{
            font-size: 1.5rem !important;
        }}
        
        .coffee-header p {{
            font-size: 0.75rem !important;
            color: {WHITE} !important;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5) !important;
        }}
        
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4 {{
            color: {COFFEE_BROWN} !important;
            font-weight: bold !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
            color: {CREAM} !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
            color: {WHITE} !important;
            font-size: 0.85rem !important;
            line-height: 1.35 !important;
            letter-spacing: 0.1px;
        }}
        
        .stMarkdown, 
        .stMarkdown p, 
        .stMarkdown li {{
            color: {DARK_BROWN} !important;
        }}
        
        .stButton > button {{
            font-size: 0.7rem !important;
            padding: 0.3rem 0.5rem !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            height: auto !important;
            min-height: 40px !important;
        }}

        [data-testid="stSidebar"] button {{
            font-size: 0.9rem !important;
            padding: 0.55rem 0.8rem !important;
            min-height: 44px !important;
            border: 3px solid {HONEY} !important;
            border-radius: 12px !important;
        }}
        
        [data-testid="stSidebar"] {{
            width: 280px !important;
        }}
        
        .memory-status {{
            display: block !important;
            margin: 10px 0 !important;
            padding: 10px !important;
        }}
        
        .user-message, .bot-message {{
            max-width: 85% !important;
            font-size: 0.85rem !important;
        }}
        
        .source-card {{
            font-size: 0.7rem !important;
        }}
        
        .footer {{
            font-size: 0.6rem !important;
            padding: 10px !important;
        }}
    }}
    
    @media (max-width: 480px) {{
        .stButton > button {{
            font-size: 0.6rem !important;
            padding: 0.2rem 0.3rem !important;
        }}

        [data-testid="stSidebar"] button {{
            font-size: 0.85rem !important;
            padding: 0.5rem 0.7rem !important;
            min-height: 42px !important;
        }}
        
        .user-message, .bot-message {{
            max-width: 90% !important;
            font-size: 0.8rem !important;
        }}
        
        h3 {{
            font-size: 1rem !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def has_relevant_context(chunks, min_score: float = 0.25):
    return any(c.get("similarity_score", 0) >= min_score for c in chunks)

def is_no_answer_response(response_text: str):
    response_lower = response_text.lower()
    indicators = [
        "couldn't find", "cannot answer", "only have information",
        "no relevant documents", "not in the available"
    ]
    return any(ind in response_lower for ind in indicators)

def remove_source_number_tags(response_text: str):
    cleaned = re.sub(r"\s*\(\s*source\s*\d+\s*\)", "", response_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*source\s*\d+\b", "", cleaned, flags=re.IGNORECASE)
    return cleaned

def set_search_input(question: str):
    st.session_state["input"] = question

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "☕ <strong>Welcome to Brew & Ask!</strong><br><br>I'm your friendly assistant for Ghana's election results and budget information. Grab a coffee and ask me anything!<br><br><strong>What I can help with:</strong><ul style='margin: 6px 0 10px 20px; padding: 0;'><li>📊 Ghana Election Results (2016, 2020)</li><li>📄 2025 Budget Statement</li></ul><strong>How to ask:</strong> Just type your question below like you're talking to a friend!"}
    ]

if "pipeline" not in st.session_state:
    with st.spinner("☕ Brewing up some answers..."):
        st.session_state.pipeline = GhanaRAGPipeline()
        st.session_state.feedback_loop = GhanaFeedbackLoop()

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "last_feedback_id" not in st.session_state:
    st.session_state.last_feedback_id = None

# Header
st.markdown(
    f"""
    <div class="coffee-header">
        <h1>☕ Brew & Ask</h1>
        <p>Your friendly Ghana Elections & Budget Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.markdown(
        f"""
        <div style=\"color:{WHITE}; font-weight:700; font-size:0.9rem; line-height:1.35; text-shadow:0 1px 2px rgba(0,0,0,0.35); margin-bottom:0.2rem;\">
            Made with ❤️ by Emmanuella Uwudia
        </div>
        <div style=\"color:{CREAM}; font-weight:600; font-size:0.82rem; line-height:1.35; text-shadow:0 1px 2px rgba(0,0,0,0.25);\">
            Index:10012200008 | CS4241 - Introduction to AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color:{CREAM}; margin: 0.75rem 0 0.4rem 0;'>What's on the menu?</h3>", unsafe_allow_html=True)
    st.info("**Election Results**\n\nHistorical voting data from past Ghana elections")
    st.info("**2025 Budget**\n\nOfficial government budget document")
    
    st.markdown("---")
    st.markdown(f"<h3 style='color:{CREAM}; margin: 0.75rem 0 0.4rem 0;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    
    k_value = st.slider("How many sources to check?", 3, 10, 5)
    use_expansion = st.checkbox("🔍 Smart Search", value=True)
    show_debug = st.checkbox("📋 Show my work", value=True)
    
    st.markdown("---")
    st.markdown(f"<h3 style='color:{CREAM}; margin: 0.75rem 0 0.4rem 0;'>🛠️ Behind the counter</h3>", unsafe_allow_html=True)
    st.markdown("""
    - Custom RAG engine
    - Smart search
    - FAISS vector index  
    - Groq AI
    """)
    
    st.markdown("---")
    st.markdown(f"<h3 style='color:{CREAM}; margin: 0.75rem 0 0.4rem 0;'>📝 Feedback</h3>", unsafe_allow_html=True)
    
    if st.button("📊 View Statistics", key="view_stats", use_container_width=True, type="secondary"):
        stats = st.session_state.feedback_loop.get_statistics()
        
        if stats and stats.get("total_feedback", 0) > 0:
            st.markdown(
                f"""
                <div class="stats-container">
                    <div class="stats-title">📊 Feedback Statistics</div>
                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <div class="stats-metric" style="flex: 1;">
                            <div class="stats-number">{stats.get("total_feedback", 0)}</div>
                            <div class="stats-label">Total Ratings</div>
                        </div>
                        <div class="stats-metric" style="flex: 1;">
                            <div class="stats-number">{stats.get("average_rating", 0):.1f}</div>
                            <div class="stats-label">⭐ Average Rating</div>
                        </div>
                        <div class="stats-metric" style="flex: 1;">
                            <div class="stats-number">{stats.get("total_positive", 0)}</div>
                            <div class="stats-label">👍 Positive</div>
                        </div>
                    </div>
                    <div class="stats-title" style="font-size: 0.9rem;">Rating Breakdown</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for fb in st.session_state.feedback_loop.feedback_data:
                r = fb.get("rating", 0)
                if r in rating_counts:
                    rating_counts[r] += 1
            
            for r in [5, 4, 3, 2, 1]:
                count = rating_counts.get(r, 0)
                if count > 0:
                    emoji = "😍" if r == 5 else "🙂" if r == 4 else "😐" if r == 3 else "😕" if r == 2 else "😞"
                    bar_width = min(100, (count / max(1, stats.get("total_feedback", 1))) * 100)
                    st.markdown(
                        f"""
                        <div class="rating-bar">
                            <div style="display: flex; justify-content: space-between;">
                                <span>{emoji} {r} star</span>
                                <span>{count} votes</span>
                            </div>
                            <div style="background-color: #E0E0E0; border-radius: 10px; height: 8px; margin-top: 5px;">
                                <div style="background-color: {TERRACOTTA}; width: {bar_width}%; height: 8px; border-radius: 10px;"></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.markdown(
                f'<div style="font-size: 0.7rem; color: #999; text-align: center; margin-top: 10px;">Keep rating to improve responses! ☕</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="stats-container" style="text-align: center;">
                    <div style="font-size: 2rem;">☕</div>
                    <div style="color: {DARK_BROWN}; font-weight: bold;">No feedback yet!</div>
                    <div style="font-size: 0.8rem; color: #666;">Ask a question and rate the response.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
# Chat area
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">🙋 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤗 {message["content"]}</div>', unsafe_allow_html=True)

# Input area
st.markdown("---")
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "Ask me anything about Ghana's elections or budget...",
        key="input",
        placeholder="e.g., What was the healthcare budget for 2025?",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("☕ Ask", use_container_width=True)

# Sample questions - Mobile-friendly
st.markdown(
    """
    <div style="margin: 15px 0;">
        <h3 style="color: #6F4E37; margin-bottom: 10px;">🔍 Try asking me...</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="font-weight: bold; color: #6F4E37; margin: 10px 0 5px 0;">
        🗳️ Election Questions:
    </div>
    """,
    unsafe_allow_html=True
)

election_cols = st.columns(3)
election_questions = [
    "Show me all election results for Edward Mahama",
    "What were the results in the Ashanti region?",
    "Who won the Greater Accra region in 2020?"
]

for idx, (col, q) in enumerate(zip(election_cols, election_questions)):
    col.button(
        f" {q}",
        key=f"election_{idx}",
        use_container_width=True,
        on_click=set_search_input,
        args=(q,)
    )

st.markdown(
    """
    <div style="font-weight: bold; color: #6F4E37; margin: 15px 0 5px 0;">
        📊 Budget Questions:
    </div>
    """,
    unsafe_allow_html=True
)

budget_cols = st.columns(3)
budget_questions = [
    "What does the budget say about healthcare?",
    "How much is allocated to education in 2025?",
    "What is the budget for road infrastructure?"
]

for idx, (col, q) in enumerate(zip(budget_cols, budget_questions)):
    col.button(
        f" {q}",
        key=f"budget_{idx}",
        use_container_width=True,
        on_click=set_search_input,
        args=(q,)
    )

# Process input
if send_button and user_input:
    st.session_state.last_feedback_id = None
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("☕ Brewing your answer..."):
        result = st.session_state.pipeline.process_query(
            query=user_input,
            k=k_value,
            use_expansion=use_expansion
        )
        st.session_state.last_response = result
    
    response_text = result["response"]
    response_text = remove_source_number_tags(response_text)
    retrieved_chunks = result.get("retrieved_chunks", [])
    
    has_good_chunks = has_relevant_context(retrieved_chunks, min_score=0.25)
    is_fallback = is_no_answer_response(response_text)
    can_show_sources = has_good_chunks and not is_fallback
    
    if not can_show_sources and not is_fallback:
        response_text = "☕ **Hmm, I couldn't quite find that in my knowledge base.**\n\nTry rephrasing with specific details like year, region, or ministry name. I'm here to help!"
    
    if show_debug and can_show_sources and retrieved_chunks:
        debug_section = "\n\n---\n**📌 Here's where I found that information:**\n"
        for chunk in retrieved_chunks[:3]:
            score = chunk.get("similarity_score", 0)
            
            if score >= 0.7:
                score_badge = "High confidence"
                score_icon = "🟢"
            elif score >= 0.4:
                score_badge = "Medium confidence"
                score_icon = "🟠"
            else:
                score_badge = "Low confidence"
                score_icon = "🔴"
            
            source_name = chunk.get('source', 'Unknown')
            text_preview = chunk.get('text', '')[:200]
            if len(chunk.get('text', '')) > 200:
                text_preview += "..."
            
            debug_section += f"\n• **{source_name}** | {score_icon} {score_badge} (Score: {score:.3f})\n  {text_preview}\n"
        
        response_text += debug_section
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()

# Feedback collection
if st.session_state.last_response is not None:
    current_response_id = id(st.session_state.last_response)
    if st.session_state.get("last_feedback_id") != current_response_id:
        st.markdown("---")
        st.markdown("### ☕ Was this answer helpful?")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("😞 1", key="fb_1", use_container_width=True):
                st.session_state.feedback_loop.add_feedback(
                    query=st.session_state.messages[-2]["content"],
                    response=st.session_state.last_response["response"],
                    chunks_used=[c["chunk_id"] for c in st.session_state.last_response.get("retrieved_chunks", [])],
                    rating=1
                )
                st.session_state.last_feedback_id = current_response_id
                st.success("☕ Thanks for the feedback! (1/5)")
                st.rerun()
        
        with col2:
            if st.button("😕 2", key="fb_2", use_container_width=True):
                st.session_state.feedback_loop.add_feedback(
                    query=st.session_state.messages[-2]["content"],
                    response=st.session_state.last_response["response"],
                    chunks_used=[c["chunk_id"] for c in st.session_state.last_response.get("retrieved_chunks", [])],
                    rating=2
                )
                st.session_state.last_feedback_id = current_response_id
                st.success("☕ Thanks for the feedback! (2/5)")
                st.rerun()
        
        with col3:
            if st.button("😐 3", key="fb_3", use_container_width=True):
                st.session_state.feedback_loop.add_feedback(
                    query=st.session_state.messages[-2]["content"],
                    response=st.session_state.last_response["response"],
                    chunks_used=[c["chunk_id"] for c in st.session_state.last_response.get("retrieved_chunks", [])],
                    rating=3
                )
                st.session_state.last_feedback_id = current_response_id
                st.success("☕ Thanks for the feedback! (3/5)")
                st.rerun()
        
        with col4:
            if st.button("🙂 4", key="fb_4", use_container_width=True):
                st.session_state.feedback_loop.add_feedback(
                    query=st.session_state.messages[-2]["content"],
                    response=st.session_state.last_response["response"],
                    chunks_used=[c["chunk_id"] for c in st.session_state.last_response.get("retrieved_chunks", [])],
                    rating=4
                )
                st.session_state.last_feedback_id = current_response_id
                st.success("☕ Thanks for the feedback! (4/5)")
                st.rerun()
        
        with col5:
            if st.button("😍 5", key="fb_5", use_container_width=True):
                st.session_state.feedback_loop.add_feedback(
                    query=st.session_state.messages[-2]["content"],
                    response=st.session_state.last_response["response"],
                    chunks_used=[c["chunk_id"] for c in st.session_state.last_response.get("retrieved_chunks", [])],
                    rating=5
                )
                st.session_state.last_feedback_id = current_response_id
                st.success("☕ Thanks for the feedback! (5/5)")
                st.rerun()

# INNOVATION: Conversation Memory - Mobile-friendly
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #FFF8E7; padding: 15px; border-radius: 12px; border-left: 5px solid #F0A500; margin: 10px 0;">
        <h3 style="margin: 0 0 10px 0; color: #6F4E37;">💡 Conversation Memory</h3>
        <p style="margin: 0 0 8px 0; color: #3E2723;">I remember our conversation! Ask follow-up questions like:</p>
        <ul style="margin: 0; padding-left: 20px; color: #3E2723;">
            <li>"What about education?"</li>
            <li>"How does that compare?"</li>
            <li>"Tell me more about that"</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("🧹 Clear Conversation History", key="clear_memory", use_container_width=True):
    st.session_state.pipeline.clear_conversation_memory()
    st.success("Conversation memory cleared! Starting fresh.")
    st.rerun()

# Display memory status
memory_summary = st.session_state.pipeline.get_conversation_summary()
if memory_summary["total_exchanges"] > 0:
    st.markdown(
        f"""
        <div class="memory-status">
            💬 <strong>Remembering last {memory_summary['total_exchanges']} exchanges</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.caption("💬 No conversation history yet. Ask a question!")
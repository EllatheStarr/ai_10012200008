"""
File: app.py
Author: Emmanuella Uwudia
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Streamlit UI for Brew & Ask - Warm Coffee Shop Theme
"""

import streamlit as st
import sys
import os
import re

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import GhanaRAGPipeline
from src.innovation_feedback import GhanaFeedbackLoop

# Page configuration
st.set_page_config(
    page_title="Brew & Ask - Your Friendly Assistant",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Warm Coffee Shop Colors
CREAM = "#FFF8E7"          # Warm cream background
COFFEE_BROWN = "#6F4E37"   # Rich coffee brown
LATTE = "#C4A484"          # Soft latte
TERRACOTTA = "#E2725B"     # Warm terracotta accent
HONEY = "#F0A500"          # Honey yellow
DARK_BROWN = "#3E2723"     # Dark coffee for text
WHITE = "#FFFFFF"

# Custom CSS for Coffee Shop Theme
st.markdown(f"""
<style>
    /* Main background - warm cream */
    .main {{
        background-color: {CREAM};
    }}
    
    .stApp {{
        background-color: {CREAM};
    }}
    
    /* Header - coffee shop sign style */
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
    }}
    
    /* User message - warm and friendly */
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
    
    /* Bot message - like a coffee chat */
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
    
    /* Source card - like a receipt/note */
    .source-card {{
        background-color: {WHITE};
        border-left: 4px solid {TERRACOTTA};
        padding: 12px;
        margin: 10px 0;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        font-size: 0.85rem;
    }}
    
    /* Score badges - friendly colors */
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
    
    /* Button styling - like coffee shop buttons */
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
    
    /* View Stats button specific styling */
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
    
    /* Sidebar - like a coffee shop menu board */
    [data-testid="stSidebar"] {{
        background-color: {COFFEE_BROWN};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {CREAM};
    }}
    
    [data-testid="stSidebar"] .stAlert {{
        background-color: {DARK_BROWN};
        border-left-color: {HONEY};
    }}
    
    /* Input field - like writing an order */
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
    
    /* Slider */
    [data-testid="stSlider"] {{
        color: {HONEY};
    }}
    
    /* Checkbox */
    .stCheckbox label {{
        color: {CREAM};
    }}
    
    /* Info boxes */
    .stAlert {{
        background-color: {DARK_BROWN};
        border-left-color: {HONEY};
        color: {CREAM};
        border-radius: 12px;
    }}
    
    /* Headers */
    h1, h2, h3, h4 {{
        color: {COFFEE_BROWN};
        font-weight: 600;
    }}
    
    /* Divider */
    hr {{
        border-color: {LATTE};
        margin: 20px 0;
    }}
    
    /* Stats container styling */
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
</style>
""", unsafe_allow_html=True)

def has_relevant_context(chunks, min_score: float = 0.25):
    """Return True when at least one retrieved chunk has acceptable relevance."""
    return any(c.get("similarity_score", 0) >= min_score for c in chunks)

def is_no_answer_response(response_text: str):
    """Detect fallback responses where sources should not be shown."""
    response_lower = response_text.lower()
    indicators = [
        "couldn't find", "cannot answer", "only have information",
        "no relevant documents", "not in the available"
    ]
    return any(ind in response_lower for ind in indicators)

def remove_source_number_tags(response_text: str):
    """Remove model artifacts like '(Source 1)' or 'Source 2' from responses."""
    cleaned = re.sub(r"\s*\(\s*source\s*\d+\s*\)", "", response_text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*source\s*\d+\b", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def set_search_input(question: str):
    """Prefill the search box from a quick-question button click."""
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
st.markdown(f"""
<div class="coffee-header">
    <h1>☕ Brew & Ask</h1>
    <p>Your friendly Ghana Elections & Budget Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.caption("Made with ❤️ by Emmanuella Uwudia")
    st.caption("Index:10012200008 | CS4241 - Introduction to AI")

    st.markdown("## What's on the menu?")
    st.info("**Election Results**\n\nHistorical voting data from past Ghana elections")
    st.info("**2025 Budget**\n\nOfficial government budget document")
    
    st.markdown("---")
    st.markdown("## ⚙️ Settings")
    
    k_value = st.slider("How many sources to check?", 3, 10, 5)
    use_expansion = st.checkbox("🔍 Smart Search", value=True)
    show_debug = st.checkbox("📋 Show my work", value=True)
    
    st.markdown("---")
    st.markdown("## 🛠️ Behind the counter")
    st.markdown("""
    - Custom RAG engine
    - Smart search
    - FAISS vector index  
    - Groq AI
    """)
    
    st.markdown("---")
    st.markdown("## 📝 Feedback")
    
    # View stats button with styled container
    if st.button("📊 View Statistics", key="view_stats", use_container_width=True):
        stats = st.session_state.feedback_loop.get_statistics()
        
        if stats and stats.get("total_feedback", 0) > 0:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)
            
            # Count ratings from feedback data
            rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for fb in st.session_state.feedback_loop.feedback_data:
                r = fb.get("rating", 0)
                if r in rating_counts:
                    rating_counts[r] += 1
            
            # Display rating bars
            for r in [5, 4, 3, 2, 1]:
                count = rating_counts.get(r, 0)
                if count > 0:
                    emoji = "😍" if r == 5 else "🙂" if r == 4 else "😐" if r == 3 else "😕" if r == 2 else "😞"
                    bar_width = min(100, (count / max(1, stats.get("total_feedback", 1))) * 100)
                    st.markdown(f"""
                    <div class="rating-bar">
                        <div style="display: flex; justify-content: space-between;">
                            <span>{emoji} {r} star</span>
                            <span>{count} votes</span>
                        </div>
                        <div style="background-color: #E0E0E0; border-radius: 10px; height: 8px; margin-top: 5px;">
                            <div style="background-color: {TERRACOTTA}; width: {bar_width}%; height: 8px; border-radius: 10px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown(f'<div style="font-size: 0.7rem; color: #999; text-align: center; margin-top: 10px;">Keep rating to improve responses! ☕</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stats-container" style="text-align: center;">
                <div style="font-size: 2rem;">☕</div>
                <div style="color: {DARK_BROWN}; font-weight: bold;">No feedback yet!</div>
                <div style="font-size: 0.8rem; color: #666;">Ask a question and rate the response.</div>
            </div>
            """, unsafe_allow_html=True)
    
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
    user_input = st.text_input("Ask me anything about Ghana's elections or budget...", key="input", placeholder="e.g., What was the healthcare budget for 2025?", label_visibility="collapsed")

with col2:
    send_button = st.button("☕ Ask", use_container_width=True)

# Sample questions - Balanced between elections and budget
st.markdown("### 🔍 Try asking me...")

# Create two rows for better organization
st.markdown("**Election Questions:**")
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

st.markdown("**Budget Questions:**")
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
    # Reset feedback tracking for new question
    st.session_state.last_feedback_id = None
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process through pipeline
    with st.spinner("☕ Brewing your answer..."):
        result = st.session_state.pipeline.process_query(
            query=user_input,
            k=k_value,
            use_expansion=use_expansion
        )
        st.session_state.last_response = result
    
    # Format response
    response_text = result["response"]
    response_text = remove_source_number_tags(response_text)
    retrieved_chunks = result.get("retrieved_chunks", [])
    
    # Check if this is a valid answer
    has_good_chunks = has_relevant_context(retrieved_chunks, min_score=0.25)
    is_fallback = is_no_answer_response(response_text)
    can_show_sources = has_good_chunks and not is_fallback
    
    # If no good answer found, provide helpful message
    if not can_show_sources and not is_fallback:
        response_text = "☕ **Hmm, I couldn't quite find that in my knowledge base.**\n\nTry rephrasing with specific details like year, region, or ministry name. I'm here to help!"
    
    # Add debug source info with enhanced score display
    if show_debug and can_show_sources and retrieved_chunks:
        debug_section = "\n\n---\n**📌 Here's where I found that information:**\n"
        for chunk in retrieved_chunks[:3]:
            score = chunk.get("similarity_score", 0)
            
            # Determine score badge and icon
            if score >= 0.7:
                score_badge = "High confidence"
                score_icon = "🟢"
            elif score >= 0.4:
                score_badge = "Medium confidence"
                score_icon = "🟠"
            else:
                score_badge = "Low confidence"
                score_icon = "🔴"
            
            # Get source name
            source_name = chunk.get('source', 'Unknown')
            
            # Get text preview (first 200 chars for more context)
            text_preview = chunk.get('text', '')[:200]
            if len(chunk.get('text', '')) > 200:
                text_preview += "..."
            
            # Format the source entry
            debug_section += f"\n• **{source_name}** | {score_icon} {score_badge} (Score: {score:.3f})\n  {text_preview}\n"
        
        response_text += debug_section
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    st.rerun()

# Feedback collection - appears after each response
if st.session_state.last_response is not None:
    # Check if feedback hasn't been given for this response
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

# INNOVATION: Clear conversation memory button
st.markdown("---")
st.markdown("## 💡 Conversation Memory")
st.markdown("""
I remember our conversation! Ask follow-up questions like:
- "What about education?"
- "How does that compare?"
- "Tell me more about that"
""")

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

"""
File: components.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Reusable UI components for Brew & Ask
"""

import streamlit as st
import json
from datetime import datetime

# Ghana flag colors
GHANA_RED = "#CE1126"
GHANA_GOLD = "#FCD116"
GHANA_GREEN = "#006B3F"
GHANA_BLACK = "#000000"

def render_header():
    """Render the Ghana-themed header"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {GHANA_RED} 0%, {GHANA_RED} 33%, {GHANA_GOLD} 33%, {GHANA_GOLD} 66%, {GHANA_GREEN} 66%, {GHANA_GREEN} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🇬🇭 Brew & Ask 🇬🇭
        </h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.95;">
            Ghana Elections & Budget Assistant | <em>"Fa abisa abisa me"</em>
        </p>
        <p style="color: white; margin: 0.25rem 0 0 0; font-size: 0.8rem; opacity: 0.8;">
            Ask me anything about Ghana's election results or the 2025 budget statement
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with data sources and settings"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="background: {GHANA_GREEN}; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 0.5rem;">
                <span style="font-size: 2rem;">🇬🇭</span>
            </div>
            <h3 style="color: {GHANA_GREEN}; margin: 0;">Brew & Ask</h3>
            <p style="color: #666; font-size: 0.8rem;">v1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"### 📚 Data Sources")
        
        st.info(f"""
        **📊 Ghana Election Results**
        - Historical voting data
        - Multiple years and regions
        - Party performance metrics
        
        **📄 2025 Budget Statement**
        - Government spending allocations
        - Economic policies
        - Ministry budgets
        """)
        
        st.markdown("---")
        
        st.markdown(f"### ⚙️ Settings")
        
        k_value = st.slider(
            "Number of chunks (k)", 
            min_value=3, 
            max_value=10, 
            value=5,
            help="More chunks = more context but slower response"
        )
        
        use_expansion = st.toggle(
            "🔍 Query Expansion", 
            value=True,
            help="Automatically expands queries with synonyms for better retrieval"
        )
        
        show_scores = st.toggle(
            "📊 Show Similarity Scores", 
            value=True,
            help="Display confidence scores for retrieved chunks"
        )
        
        show_prompt = st.toggle(
            "📝 Show Prompt (Debug)", 
            value=False,
            help="Display the full prompt sent to the LLM"
        )
        
        st.markdown("---")
        
        st.markdown(f"### 🎯 Quick Tips")
        st.markdown("""
        **Try asking:**
        - *"What is the healthcare budget?"*
        - *"Who won the 2020 election?"*
        - *"Education spending in 2025"*
        - *"Voter turnout trends"*
        """)
        
        st.markdown("---")
        
        return {
            "k_value": k_value,
            "use_expansion": use_expansion,
            "show_scores": show_scores,
            "show_prompt": show_prompt
        }

def render_chunk_card(chunk, index):
    """Render a single retrieved chunk as a card - NO YELLOW VERSION"""
    score = chunk.get("similarity_score", 0)
    source_type = chunk.get("source_type", "unknown")
    
    # Score color - HIGH CONTRAST, CLEARLY DISTINCT COLORS
    if score >= 0.7:
        score_color = "#006B3F"      # Ghana Green
        score_bg = "#C8E6C9"         # Light green background
        score_icon = "🟢"
        score_label = "High"
    elif score >= 0.4:
        score_color = "#D32F2F"      # Deep Red-Orange (NOT yellow!)
        score_bg = "#FFCCBC"         # Light peach background
        score_icon = "🟠"
        score_label = "Medium"
    else:
        score_color = "#CE1126"      # Ghana Red
        score_bg = "#FFCDD2"         # Light red background
        score_icon = "🔴"
        score_label = "Low"
    
    # Source icon
    source_icon = "📊" if source_type == "csv" else "📄"
    
    # Truncate text
    text_preview = chunk.get('text', '')[:200]
    if len(chunk.get('text', '')) > 200:
        text_preview += "..."
    
    st.markdown(f"""
    <div style="
        background-color: white;
        border-left: 5px solid {score_color};
        padding: 14px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: bold; font-size: 0.9rem;">
                {source_icon} {chunk.get('source', 'Unknown')}
            </span>
            <span style="
                background-color: {score_bg}; 
                color: {score_color}; 
                padding: 4px 12px; 
                border-radius: 20px; 
                font-weight: bold;
                font-size: 0.8rem;
                display: inline-flex;
                align-items: center;
                gap: 5px;
            ">
                {score_icon} Score: {score:.3f} ({score_label})
            </span>
        </div>
        <div style="color: #333; line-height: 1.5; font-size: 0.85rem; margin-bottom: 8px;">
            {text_preview}
        </div>
        <div style="font-size: 0.7rem; color: #999; margin-top: 8px;">
            📍 Rank: #{index + 1} | ID: {chunk.get('chunk_id', 'N/A')}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_response_card(response_text, retrieved_chunks, show_scores=True):
    """Render the final response with sources - ONLY shows relevant sources"""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border: 1px solid #e0e0e0;
    ">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: {GHANA_GREEN}; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                <span style="color: white; font-weight: bold;">🤖</span>
            </div>
            <h3 style="margin: 0; color: {GHANA_GREEN};">Brew & Ask Response</h3>
        </div>
        <div style="line-height: 1.6; font-size: 1rem;">
            {response_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ONLY show sources if there are relevant chunks with good scores (>= 0.3)
    if show_scores and retrieved_chunks:
        # Filter out low-quality chunks (below 0.3 threshold)
        relevant_chunks = [c for c in retrieved_chunks if c.get("similarity_score", 0) >= 0.3]
        
        if relevant_chunks:
            st.markdown("---")
            st.markdown(f"### 📌 Sources Used")
            
            for i, chunk in enumerate(relevant_chunks[:5]):
                render_chunk_card(chunk, i)
        # If no relevant chunks, don't show the sources section at all

def render_prompt_card(prompt_text):
    """Render the prompt for debugging"""
    with st.expander("📝 View Prompt Sent to LLM (Debug)"):
        st.code(prompt_text, language="markdown")

def render_feedback_widget(query, response, chunks_used):
    """Render the feedback collection widget"""
    st.markdown("---")
    st.markdown(f"### Was this response helpful?")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    feedback_value = st.session_state.get("feedback_value", None)
    
    if col1.button("😞 1", key="fb_1", use_container_width=True):
        feedback_value = 1
    if col2.button("😕 2", key="fb_2", use_container_width=True):
        feedback_value = 2
    if col3.button("😐 3", key="fb_3", use_container_width=True):
        feedback_value = 3
    if col4.button("🙂 4", key="fb_4", use_container_width=True):
        feedback_value = 4
    if col5.button("😍 5", key="fb_5", use_container_width=True):
        feedback_value = 5
    
    if feedback_value:
        st.session_state.feedback_value = feedback_value
        return feedback_value
    
    return None

def render_sample_questions():
    """Render sample question buttons"""
    st.markdown("---")
    st.markdown(f"### 🔍 Try these questions")
    
    sample_questions = [
        "What is the healthcare budget for 2025?",
        "Which party won the 2020 election?",
        "How much is allocated to education?",
        "What were the voter turnout figures?",
        "Tell me about road infrastructure spending"
    ]
    
    cols = st.columns(5)
    for i, q in enumerate(sample_questions):
        if cols[i].button(q, key=f"sample_{i}", use_container_width=True):
            return q
    
    return None

def render_footer():
    """Render the footer"""
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.8rem;
    ">
        <p>
            🇬🇭 <strong>Brew & Ask</strong> | Powered by Custom RAG Architecture<br>
            <small>Data Sources: Ghana Election Results & 2025 Budget Statement</small>
        </p>
        <p style="margin-top: 10px;">
            <small>⚠️ Answers are grounded in official documents. No hallucinations guaranteed.</small>
        </p>
        <p style="margin-top: 10px; color: {GHANA_GREEN}; font-weight: bold;">
            Built with ❤️ by Emmanuella Uuwdia
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_loading_animation():
    """Render Ghana-themed loading animation"""
    with st.spinner("🟡 Me reyɛ adwuma... (Working on it)"):
        import time
        time.sleep(0.5)

def render_error_message(error_text):
    """Render error message with Ghana flair"""
    st.markdown(f"""
    <div style="
        background-color: #ffebee;
        border-left: 4px solid {GHANA_RED};
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    ">
        <span style="font-weight: bold;">😔 Chale! Something went wrong.</span><br>
        <span style="font-size: 0.9rem;">{error_text}</span><br>
        <span style="font-size: 0.8rem; color: #666;">Please try again or rephrase your question.</span>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_message():
    """Render the welcome message for new users"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {GHANA_GOLD}20, {GHANA_GREEN}20);
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        text-align: center;
    ">
        <span style="font-size: 3rem;">🇬🇭</span>
        <h3 style="color: {GHANA_GREEN};">Akwaaba! Welcome to Brew & Ask</h3>
        <p>I'm your AI assistant for Ghana's election results and budget information.</p>
        <p style="font-size: 0.9rem; color: #666;">
            Try asking me a question below, or click one of the sample questions.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_statistics_dashboard(stats):
    """Render statistics dashboard in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 📊 System Stats")
        
        if stats and "total_queries" in stats:
            st.metric("Total Queries", stats.get("total_queries", 0))
            st.metric("Avg Response Time", f"{stats.get('average_total_time', 0):.1f}s")
            st.metric("Success Rate", f"{stats.get('success_rate', 0)*100:.0f}%")
        
        st.markdown("---")
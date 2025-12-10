"""
VANCO AI - Enterprise Client Relationship Agent
Streamlit UI for managing enterprise client relationships
Powered by LangChain, LangGraph, OpenAI & Supermemory
"""
import os
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

from agent import CRMAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="VANCO AI - Enterprise Client Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling - Modern Human-Centered Vanco AI Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0.5rem 2rem;
        background: linear-gradient(180deg, #fafbfc 0%, #f0f4f8 100%);
    }
    
    /* Hide default Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1a1a2e;
    }
    
    p, span, div, input, textarea, button {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 50%, #252547 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255,255,255,0.9);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: rgba(255,255,255,0.8) !important;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .logo-container img {
        max-width: 160px;
        height: auto;
        filter: brightness(1.1);
    }
    
    .logo-tagline {
        color: rgba(255,255,255,0.6);
        font-size: 11px;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }
    
    /* Welcome Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 1rem 0 2rem 0;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section h1 {
        color: white !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-section p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    /* Client Header Card */
    .client-header-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .client-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: white;
        font-weight: 600;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .client-info h2 {
        margin: 0 0 4px 0;
        font-size: 1.5rem;
        color: #1a1a2e;
    }
    
    .client-info p {
        margin: 0;
        color: #6b7280;
        font-size: 0.95rem;
    }
    
    .client-badge {
        display: inline-block;
        background: #ecfdf5;
        color: #059669;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-top: 8px;
    }
    
    /* Chat Container */
    .chat-wrapper {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        min-height: 400px;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 0.75rem 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background: #f7f8fa !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* User message styling */
    .stChatMessage[data-testid="chat-message-user"] [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 18px 18px 4px 18px !important;
    }
    
    /* Empty chat state */
    .empty-chat-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 16px;
        border: 2px dashed #e2e8f0;
    }
    
    .empty-chat-state h3 {
        color: #475569;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .empty-chat-state p {
        color: #94a3b8;
    }
    
    .empty-chat-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 4px;
    }
    
    /* Section Cards */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .section-header h4 {
        margin: 0;
        font-size: 1.1rem;
        color: #1a1a2e;
    }
    
    /* Meeting Cards */
    .meeting-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #10b981;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .meeting-icon {
        width: 45px;
        height: 45px;
        background: white;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
    
    .meeting-details h5 {
        margin: 0;
        color: #065f46;
        font-size: 0.95rem;
    }
    
    .meeting-details p {
        margin: 2px 0 0 0;
        color: #047857;
        font-size: 0.85rem;
    }
    
    /* Project Cards */
    .project-card {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #f59e0b;
    }
    
    .project-card h5 {
        margin: 0 0 4px 0;
        color: #92400e;
        font-size: 0.95rem;
    }
    
    .project-card p {
        margin: 0;
        color: #b45309;
        font-size: 0.85rem;
    }
    
    .project-value {
        background: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #d97706;
        display: inline-block;
        margin-top: 8px;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin: 3px;
        transition: transform 0.15s ease;
    }
    
    .tag:hover {
        transform: scale(1.05);
    }
    
    .tag-interest {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        color: #7c3aed;
    }
    
    .tag-service {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        color: #0369a1;
    }
    
    .tag-general {
        background: #f3f4f6;
        color: #4b5563;
    }
    
    /* Sentiment Badges */
    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .sentiment-positive {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
    }
    
    .sentiment-negative {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
    }
    
    /* Recommendation Cards */
    .recommendation-card {
        background: linear-gradient(135deg, #ede9fe 0%, #e0e7ff 100%);
        padding: 1.25rem;
        border-radius: 14px;
        text-align: center;
        border: 1px solid rgba(124, 58, 237, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(124, 58, 237, 0.15);
    }
    
    .recommendation-card h4 {
        margin: 0;
        color: #5b21b6;
        font-size: 0.95rem;
        font-weight: 600;
    }
    
    .recommendation-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Memory Cards */
    .memory-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #f1f5f9;
        transition: box-shadow 0.2s ease;
    }
    
    .memory-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .memory-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .memory-type {
        font-size: 12px;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Quick Action Buttons */
    .quick-actions {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 6px;
        gap: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .footer p {
        color: #9ca3af;
        font-size: 13px;
        margin: 4px 0;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .footer-links a {
        color: #6b7280;
        text-decoration: none;
        font-size: 13px;
        transition: color 0.2s ease;
    }
    
    .footer-links a:hover {
        color: #667eea;
    }
    
    /* Sidebar Form Styling - Improved */
    [data-testid="stSidebar"] {
        padding-top: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    
    /* Text inputs in sidebar - Dark theme */
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #1e1e2e !important;
        border: 1px solid #3d3d5c !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.75rem !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #6b6b8a !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > label {
        color: #a0a0b8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox in sidebar - Dark theme */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: #1e1e2e !important;
        border: 1px solid #3d3d5c !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        background: #1e1e2e !important;
        border-color: #3d3d5c !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > label {
        color: #a0a0b8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #a0a0b8 !important;
    }
    
    /* Dropdown menu styling - Dark theme for sidebar */
    [data-baseweb="popover"] {
        background: #1a1a2e !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
    }
    
    [data-baseweb="popover"] > div {
        background: #1a1a2e !important;
    }
    
    [data-baseweb="menu"] {
        background: #1a1a2e !important;
    }
    
    [data-baseweb="menu"] ul {
        background: #1a1a2e !important;
    }
    
    [data-baseweb="menu"] li {
        background: #1a1a2e !important;
        color: #e0e0e0 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: #2d2d4a !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="menu"] [aria-selected="true"] {
        background: #3d3d5c !important;
        color: #ffffff !important;
    }
    
    /* Option styling */
    [role="option"] {
        background: #1a1a2e !important;
        color: #e0e0e0 !important;
    }
    
    [role="option"]:hover {
        background: #2d2d4a !important;
        color: #ffffff !important;
    }
    
    [role="listbox"] {
        background: #1a1a2e !important;
        border: 1px solid #3d3d5c !important;
    }
    
    /* Sidebar button styling */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.6rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%) !important;
        transform: translateY(-1px);
    }
    
    /* Form submit button */
    [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Sidebar form container */
    [data-testid="stSidebar"] [data-testid="stForm"] {
        background: rgba(30, 30, 46, 0.5) !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #3d3d5c !important;
        margin: 1rem 0 !important;
    }
    
    /* Sidebar markdown text */
    [data-testid="stSidebar"] .stMarkdown p {
        color: #c0c0d0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #ffffff !important;
    }
    
    /* Sidebar expander styling */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: #252538 !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 14px !important;
        padding: 0.75rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: #2d2d44 !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background: #1a1a28 !important;
        border: 1px solid #3d3d5c !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader svg {
        fill: #a0a0b8 !important;
    }
    
    /* Success/Error messages in sidebar */
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34d399 !important;
    }
    
    [data-testid="stSidebar"] .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #f87171 !important;
    }
    
    /* Checkbox styling in sidebar */
    [data-testid="stSidebar"] .stCheckbox {
        background: #252538 !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox:hover {
        background: #2d2d44 !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox label {
        color: #ffffff !important;
        font-size: 14px !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox label span {
        color: #ffffff !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.4s ease-out;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .info-box p {
        margin: 0;
        color: #1e40af;
        font-size: 0.9rem;
    }
    
    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .success-box p {
        margin: 0;
        color: #065f46;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "agent" not in st.session_state:
    st.session_state.agent = None
if "customers" not in st.session_state:
    st.session_state.customers = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def initialize_agent():
    """Initialize the CRM Agent"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY not set in environment variables")
        st.info("Please set your OpenAI API key in a .env file or environment variables")
        return False

    try:
        st.session_state.agent = CRMAgent(
            openai_api_key=api_key,
            use_local_memory=True  # Using local memory for development
        )
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {str(e)}")
        return False


def add_customer(customer_id: str, customer_name: str, email: str = "", company: str = "", industry: str = ""):
    """Add a new enterprise client"""
    if customer_id in st.session_state.customers:
        st.warning(f"Client {customer_id} already exists")
        return False

    st.session_state.customers[customer_id] = {
        "name": customer_name,
        "email": email,
        "company": company,
        "industry": industry,
        "created_at": datetime.now().isoformat()
    }
    st.session_state.chat_history[customer_id] = []
    return True


def display_chat_messages(customer_id: str):
    """Display chat history with human-centered styled messages"""
    history = st.session_state.chat_history.get(customer_id, [])
    customer_info = st.session_state.customers.get(customer_id, {})
    customer_name = customer_info.get('name', 'Client')

    if not history:
        st.markdown(f"""
        <div class='empty-chat-state'>
            <div class='empty-chat-icon'>👋</div>
            <h3>Start a Conversation with {customer_name}</h3>
            <p>Begin discussing AI solutions, projects, or services.<br>
            Every interaction builds their profile and helps personalize recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Display messages using Streamlit's chat_message with custom avatars
    # Use local Vanco logo for bot avatar
    import os
    vanco_logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "vanco_logo.png")
    
    for msg in history:
        role = msg.get("role")
        text = msg.get("message")
        timestamp = msg.get("timestamp", "")

        if role == "customer":
            with st.chat_message("user", avatar="👤"):
                st.write(text)
                st.caption(f"🕐 {timestamp}")
        else:
            # Use local logo if exists, otherwise use URL
            if os.path.exists(vanco_logo_path):
                with st.chat_message("assistant", avatar=vanco_logo_path):
                    st.write(text)
                    st.caption(f"🕐 {timestamp}")
            else:
                with st.chat_message("assistant", avatar="https://www.vanco.ai/images/Vanco-logo.svg"):
                    st.write(text)
                    st.caption(f"🕐 {timestamp}")


def display_customer_profile(customer_id: str):
    """Display enterprise client profile information with modern styling"""
    try:
        profile = st.session_state.agent.get_customer_profile(customer_id)
        if not profile:
            st.markdown("""
            <div class="info-box">
                <p>📋 <strong>No profile data available yet.</strong> Start a conversation to build this client's profile automatically!</p>
            </div>
            """, unsafe_allow_html=True)
            return

        # Metrics Row
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💰</div>
                <div class="metric-value">${profile.get('project_value', profile.get('total_spent', 0)):,.0f}</div>
                <div class="metric-label">Project Value</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">💬</div>
                <div class="metric-value">{profile.get('interaction_count', 0)}</div>
                <div class="metric-label">Interactions</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            sentiment = profile.get('sentiment_trend', 'neutral')
            emoji = "😊" if sentiment == "positive" else "😐" if sentiment == "neutral" else "😞"
            sentiment_class = f"sentiment-{sentiment}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">{emoji}</div>
                <div class="metric-value">{sentiment.capitalize()}</div>
                <div class="metric-label">Sentiment</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            meetings_count = len(profile.get('scheduled_meetings', []))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-value">{meetings_count}</div>
                <div class="metric-label">Meetings</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Two column layout
        col_left, col_right = st.columns(2)

        with col_left:
            # Client Information Card
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">🏢</span>
                    <h4>Client Information</h4>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p><strong>Company:</strong> {profile.get('company') or 'Not identified yet'}</p>
                <p><strong>Industry:</strong> {profile.get('industry') or 'Not identified yet'}</p>
                <p><strong>Email:</strong> {profile.get('email') or 'Not provided'}</p>
                <p><strong>Phone:</strong> {profile.get('phone') or 'Not provided'}</p>
                <p><strong>Budget:</strong> {profile.get('estimated_budget') or 'Not discussed'}</p>
            </div>
            """, unsafe_allow_html=True)

            # AI/Tech Interests
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">🏷️</span>
                    <h4>AI/Tech Interests</h4>
                </div>
            """, unsafe_allow_html=True)
            preferences = profile.get('preferences', [])
            if preferences:
                tags_html = " ".join([f'<span class="tag tag-interest">#{pref}</span>' for pref in preferences])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #9ca3af;'>No interests detected yet</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Service Interests
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">🎯</span>
                    <h4>Service Interests</h4>
                </div>
            """, unsafe_allow_html=True)
            service_interests = profile.get('service_interests', [])
            if service_interests:
                for service in service_interests:
                    st.markdown(f'<span class="tag tag-service">{service}</span>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #9ca3af;'>No specific services discussed yet</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            # Scheduled Meetings
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">📅</span>
                    <h4>Scheduled Meetings</h4>
                </div>
            """, unsafe_allow_html=True)
            meetings = profile.get('scheduled_meetings', [])
            if meetings:
                for meeting in meetings:
                    st.markdown(f"""
                    <div class="meeting-card">
                        <div class="meeting-icon">📅</div>
                        <div class="meeting-details">
                            <h5>{meeting.get('date', 'TBD')} at {meeting.get('time', 'TBD')}</h5>
                            <p>{meeting.get('purpose', 'Project Discussion')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #9ca3af;'>No meetings scheduled</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Proposed Projects
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">📋</span>
                    <h4>Proposed Projects</h4>
                </div>
            """, unsafe_allow_html=True)
            proposed = profile.get('proposed_projects', [])
            if proposed:
                for project in proposed:
                    value_str = f"${project.get('estimated_value'):,.0f}" if project.get('estimated_value') else "TBD"
                    st.markdown(f"""
                    <div class="project-card">
                        <h5>🚀 {project.get('project_name', 'New Project')}</h5>
                        <p>{project.get('description', 'No description')}</p>
                        <span class="project-value">{value_str}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #9ca3af;'>No projects proposed yet</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Support Requests
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">⚠️</span>
                    <h4>Support Requests</h4>
                </div>
            """, unsafe_allow_html=True)
            issues = profile.get('issues_reported', [])
            if issues:
                for issue in issues[-3:]:
                    status = "✅ Resolved" if issue.get('resolved') else "🔴 Open"
                    with st.expander(f"{status} {issue.get('description', '')[:40]}..."):
                        st.write(f"**Description:** {issue.get('description')}")
                        st.write(f"**Category:** {issue.get('category', 'N/A')}")
                        st.write(f"**Severity:** {issue.get('severity', 'N/A')}")
            else:
                st.markdown("""
                <div class="success-box">
                    <p>🎉 No support requests — all good!</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Key Requirements Section
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span style="font-size: 1.25rem;">✅</span>
                <h4>Key Requirements Identified</h4>
            </div>
        """, unsafe_allow_html=True)
        requirements = profile.get('key_requirements', [])
        if requirements:
            cols = st.columns(2)
            for idx, req in enumerate(requirements):
                with cols[idx % 2]:
                    st.markdown(f"✓ {req}")
        else:
            st.markdown("<p style='color: #9ca3af;'>No specific requirements captured yet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Project History
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span style="font-size: 1.25rem;">🚀</span>
                <h4>Completed AI Projects</h4>
            </div>
        """, unsafe_allow_html=True)
        projects = profile.get('project_history', profile.get('purchase_history', []))
        if projects:
            for project in projects[-5:]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{project.get('project_name', project.get('product_name', 'N/A'))}**")
                with col2:
                    st.write(f"${project.get('value', project.get('amount', 0)):,.0f}")
                with col3:
                    st.write(f"📁 {project.get('service_category', project.get('category', 'N/A'))}")
        else:
            st.markdown("<p style='color: #9ca3af;'>No completed projects yet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Tags Section
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span style="font-size: 1.25rem;">🏷️</span>
                <h4>Client Tags</h4>
            </div>
        """, unsafe_allow_html=True)
        tags = profile.get('tags', [])
        if tags:
            tags_html = " ".join([f'<span class="tag tag-general">{tag}</span>' for tag in tags])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #9ca3af;'>No tags assigned</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error displaying profile: {str(e)}")


def display_memory_history(customer_id: str):
    """Display memory history and interaction details with modern styling"""
    st.markdown("### 🧠 AI Memory & Interaction History")
    st.markdown("""
    <div class="info-box">
        <p>💡 The AI agent stores and retrieves relevant memories from past conversations to provide personalized, context-aware responses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get memories from agent
    memories = st.session_state.agent.get_customer_memories(customer_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span style="font-size: 1.25rem;">📝</span>
                <h4>Stored Memories</h4>
            </div>
        """, unsafe_allow_html=True)
        
        if memories:
            for idx, memory in enumerate(memories[-10:], 1):
                memory_type = memory.get('type', 'unknown')
                content = memory.get('content', '')
                metadata = memory.get('metadata', {})
                timestamp = metadata.get('timestamp', '')[:16] if metadata.get('timestamp') else ''
                
                icon = "💬" if memory_type == "customer_query" else "🤖" if memory_type == "agent_response" else "📌"
                type_label = "Client Query" if memory_type == "customer_query" else "Agent Response" if memory_type == "agent_response" else memory_type.replace("_", " ").title()
                
                with st.expander(f"{icon} Memory #{idx} — {type_label}"):
                    st.markdown(f"""
                    <div class="memory-card">
                        <div class="memory-header">
                            <span class="memory-type">{type_label}</span>
                            {f'<span style="color: #9ca3af; font-size: 12px;">🕐 {timestamp}</span>' if timestamp else ''}
                        </div>
                        <p style="margin: 0; color: #374151;">{content[:300]}{'...' if len(content) > 300 else ''}</p>
                        {f'<p style="margin-top: 8px;"><span class="sentiment-badge sentiment-{metadata.get("sentiment", "neutral")}">Sentiment: {metadata.get("sentiment", "N/A")}</span></p>' if metadata.get('sentiment') else ''}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p style='color: #9ca3af; text-align: center; padding: 2rem;'>
                No memories stored yet.<br>Start chatting to build AI memory!
            </p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span style="font-size: 1.25rem;">📊</span>
                <h4>Profile Summary</h4>
            </div>
        """, unsafe_allow_html=True)
        
        profile_summary = st.session_state.agent.get_profile_summary(customer_id)
        st.code(profile_summary, language=None)
        
        st.markdown("</div>", unsafe_allow_html=True)


def display_recommendations(customer_id: str):
    """Display AI service recommendations with modern styling"""
    st.markdown("### 🎯 AI-Powered Service Recommendations")
    st.markdown("""
    <div class="info-box">
        <p>💡 Personalized recommendations are generated based on the client's project history, interests, and conversation context.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.agent:
        # Try recommend_services first, fallback to recommend_products for backward compatibility
        try:
            recommendations = st.session_state.agent.profile_builder.recommend_services(customer_id)
        except AttributeError:
            recommendations = st.session_state.agent.profile_builder.recommend_products(customer_id)
        
        if recommendations:
            st.markdown("""
            <div class="section-card">
                <div class="section-header">
                    <span style="font-size: 1.25rem;">✨</span>
                    <h4>Recommended Services</h4>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<p style='color: #6b7280; margin-bottom: 1rem;'>Based on this client's project history and AI/tech interests:</p>", unsafe_allow_html=True)
            
            cols = st.columns(min(len(recommendations), 3))
            recommendation_icons = ["🤖", "🧠", "📊", "☁️", "💡", "🔧"]
            for idx, rec in enumerate(recommendations[:6]):
                with cols[idx % 3]:
                    icon = recommendation_icons[idx % len(recommendation_icons)]
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="recommendation-icon">{icon}</div>
                        <h4>{rec}</h4>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="section-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">💡</div>
                <h4 style="color: #374151;">No Recommendations Yet</h4>
                <p style="color: #9ca3af;">As the client interacts more, personalized AI service recommendations will appear!</p>
                
                <div style="margin-top: 2rem; text-align: left; max-width: 400px; margin-left: auto; margin-right: auto;">
                    <p style="color: #6b7280; font-weight: 600; margin-bottom: 0.5rem;">📈 How to get recommendations:</p>
                    <ul style="color: #9ca3af; padding-left: 1.5rem;">
                        <li>Chat with the client about their AI needs</li>
                        <li>Add projects to build their history</li>
                        <li>The AI learns from every conversation</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)


# Main Streamlit App
def main():
    # Sidebar
    with st.sidebar:
        # Vanco AI Logo - Clean header
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;">
            <img src="https://www.vanco.ai/images/Vanco-logo.svg" alt="Vanco AI" style="max-width: 140px; height: auto;">
            <p style="color: rgba(255,255,255,0.5); font-size: 11px; margin-top: 8px; letter-spacing: 1px;">ENTERPRISE AI SOLUTIONS</p>
        </div>
        """, unsafe_allow_html=True)

        # Initialize Agent Button
        if st.button(" Initialize Agent", key="init_btn", use_container_width=True, type="primary"):
            with st.spinner("🔄 Initializing..."):
                if initialize_agent():
                    st.success("✅ Ready!")
                else:
                    st.error("❌ Failed")

        if st.session_state.agent is None:
            st.markdown("""
            <div style="background: rgba(251,191,36,0.15); padding: 0.75rem 1rem; border-radius: 8px; border-left: 3px solid #fbbf24; margin-top: 0.5rem;">
                <p style="margin: 0; color: #fcd34d; font-size: 13px;">⚠️ Click above to initialize the agent</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        # Divider
        st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.1); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Client Management Header
        st.markdown("""
        <p style="color: rgba(255,255,255,0.5); font-size: 11px; letter-spacing: 1px; margin-bottom: 0.75rem;">CLIENT MANAGEMENT</p>
        """, unsafe_allow_html=True)

        # Add Client Form - Using checkbox toggle instead of expander
        show_form = st.checkbox("➕ Add New Client", value=False, key="show_add_client_form")
        
        if show_form:
            with st.form("new_customer_form", clear_on_submit=True):
                cust_id = st.text_input("Client ID", placeholder="client_001", label_visibility="collapsed")
                cust_name = st.text_input("Contact Name", placeholder="Contact Name", label_visibility="collapsed")
                cust_company = st.text_input("Company", placeholder="Company Name", label_visibility="collapsed")
                cust_industry = st.selectbox("Industry", 
                    ["Select Industry", "Automotive", "Healthcare", "Finance & Banking", "Retail & E-commerce", 
                     "Manufacturing", "Logistics", "Technology", "Energy", "Telecommunications", "Media & Entertainment"],
                    label_visibility="collapsed"
                )
                cust_email = st.text_input("Email", placeholder="email@company.com", label_visibility="collapsed")
                submitted = st.form_submit_button("Add Client", use_container_width=True, type="primary")

                if submitted and cust_id and cust_name:
                    industry_value = cust_industry if cust_industry != "Select Industry" else ""
                    if add_customer(cust_id, cust_name, cust_email, cust_company, industry_value):
                        st.success(f"✅ Added!")

        # Client selection
        if st.session_state.customers:
            st.markdown("""
            <p style="color: rgba(255,255,255,0.7); font-size: 13px; margin: 1rem 0 0.5rem 0; font-weight: 500;">Select Client</p>
            """, unsafe_allow_html=True)
            
            customer_options = {
                f"{info['name']} • {info.get('company', cid)}": cid
                for cid, info in st.session_state.customers.items()
            }
            selected = st.selectbox(
                "Choose client", 
                options=list(customer_options.keys()), 
                key="customer_select", 
                label_visibility="collapsed"
            )
            if selected:
                st.session_state.current_customer = customer_options[selected]
            
            # Client count badge
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem; 
                        background: rgba(102,126,234,0.15); border-radius: 8px; margin-top: 1rem;">
                <span style="font-size: 1.5rem; font-weight: 700; color: #818cf8;">{len(st.session_state.customers)}</span>
                <span style="color: rgba(255,255,255,0.6); font-size: 12px;">Active Clients</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; 
                        border: 1px dashed rgba(255,255,255,0.15); margin-top: 0.5rem;">
                <p style="margin: 0; color: rgba(255,255,255,0.5); font-size: 13px;">No clients yet</p>
                <p style="margin: 0.25rem 0 0 0; color: rgba(255,255,255,0.3); font-size: 11px;">Add your first client above</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.1); margin: 1.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            <p style="color: rgba(255,255,255,0.3); font-size: 10px; margin: 0;">Powered by</p>
            <p style="color: rgba(255,255,255,0.5); font-size: 11px; margin: 4px 0 0 0;">LangChain • LangGraph • OpenAI</p>
        </div>
        """, unsafe_allow_html=True)

    # Main content area
    if st.session_state.current_customer is None:
        # Welcome Hero Section
        st.markdown("""
        <div class="hero-section animate-fade-in">
            <img src="https://www.vanco.ai/images/Vanco-logo.svg" alt="Vanco AI" style="max-width: 200px; margin-bottom: 1.5rem; filter: brightness(10);">
            <h1>Enterprise Client Relationship Agent</h1>
            <p>Your AI-powered partner for building meaningful client relationships.<br>
            From concept to production — empowering enterprises to scale smarter.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="section-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                <h4>Intelligent Memory</h4>
                <p style="color: #6b7280; font-size: 14px;">Never forget a client interaction. AI-powered memory retrieves context from every conversation.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="section-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4>Smart Profiles</h4>
                <p style="color: #6b7280; font-size: 14px;">Automatically build detailed client profiles with interests, requirements, and sentiment tracking.</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="section-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h4>AI Recommendations</h4>
                <p style="color: #6b7280; font-size: 14px;">Get personalized service recommendations based on client needs and project history.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #9ca3af; font-size: 14px;">👈 Select or add a client from the sidebar to get started</p>
        </div>
        """, unsafe_allow_html=True)
        return

    customer_id = st.session_state.current_customer
    customer_info = st.session_state.customers.get(customer_id, {})

    # Client Header Card
    client_initial = customer_info.get('name', 'C')[0].upper()
    st.markdown(f"""
    <div class="client-header-card animate-fade-in">
        <div class="client-avatar">{client_initial}</div>
        <div class="client-info" style="flex-grow: 1;">
            <h2>{customer_info.get('name', 'Unknown Client')}</h2>
            <p>🏢 {customer_info.get('company', 'Company not specified')} • 📧 {customer_info.get('email') or 'No email'}</p>
            <span class="client-badge">🏭 {customer_info.get('industry') or 'Industry not set'}</span>
        </div>
        <div style="text-align: right;">
            <div class="metric-card" style="padding: 1rem 1.5rem;">
                <div class="metric-value">{len(st.session_state.chat_history.get(customer_id, []))}</div>
                <div class="metric-label">Messages</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs with better styling
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Conversation", "💼 Client Profile", "🧠 AI Memory", "🎯 Recommendations"])

    with tab1:
        # Chat container with improved styling
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
        
        chat_container = st.container()
        
        with chat_container:
            display_chat_messages(customer_id)
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # Input section with chat_input for better UX
        user_message = st.chat_input(
            placeholder=f"Message {customer_info.get('name', 'client')}... Type your message and press Enter",
            key="chat_input"
        )
        
        if user_message:
            # Process message directly
            customer_name = customer_info.get('name', 'Customer')
            
            with st.spinner("💭 Composing personalized response..."):
                try:
                    response = st.session_state.agent.process_customer_message(
                        customer_id=customer_id,
                        customer_name=customer_name,
                        message=user_message
                    )

                    # Store in chat history
                    st.session_state.chat_history[customer_id].append({
                        "role": "customer",
                        "message": user_message,
                        "timestamp": datetime.now().strftime("%I:%M %p")
                    })
                    st.session_state.chat_history[customer_id].append({
                        "role": "agent",
                        "message": response,
                        "timestamp": datetime.now().strftime("%I:%M %p")
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Quick action buttons with improved styling
        st.markdown("#### 💡 Conversation Starters")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🤖 AI Consulting", use_container_width=True, help="Discuss AI consulting services"):
                pass
        with col2:
            if st.button("🚀 New Project", use_container_width=True, help="Start a new project discussion"):
                pass
        with col3:
            if st.button("📅 Schedule Demo", use_container_width=True, help="Schedule a product demo"):
                pass
        with col4:
            if st.button("🗑️ Clear History", use_container_width=True, help="Clear conversation history"):
                st.session_state.chat_history[customer_id] = []
                st.rerun()

    with tab2:
        display_customer_profile(customer_id)

    with tab3:
        display_memory_history(customer_id)

    with tab4:
        display_recommendations(customer_id)

    # Footer with Vanco AI branding
    st.markdown("""
    <div class="footer">
        <img src="https://www.vanco.ai/images/Vanco-logo.svg" alt="Vanco AI" style="max-width: 120px; opacity: 0.7; margin-bottom: 1rem;">
        <p>Enterprise Client Relationship Agent</p>
        <p>Custom AI Development from Concept to Production | Trusted by 50+ Enterprises Worldwide</p>
        <div class="footer-links">
            <a href="https://www.vanco.ai" target="_blank">Website</a>
            <a href="https://www.vanco.ai/services" target="_blank">Services</a>
            <a href="https://www.vanco.ai/contactus" target="_blank">Contact Us</a>
        </div>
    
        <p style="font-size: 10px; color: #d1d5db;">© 2025 Vanco AI. All Rights Reserved.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

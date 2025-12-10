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

# Custom styling - Vanco AI Theme
st.markdown("""
<style>
    .main { padding: 1rem; }
    
    /* Chat container styling */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    
    /* Client message bubble - Vanco AI Blue */
    .customer-message {
        background-color: #1e3a5f;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        word-wrap: break-word;
    }
    
    /* Agent message bubble */
    .agent-message {
        background-color: #e9ecef;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    /* Timestamp styling */
    .message-time {
        font-size: 10px;
        color: #888;
        margin-top: 4px;
    }
    
    /* Memory card styling */
    .memory-card {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Profile card */
    .profile-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Sentiment badges */
    .sentiment-positive { 
        background-color: #d4edda; 
        color: #155724; 
        padding: 4px 12px; 
        border-radius: 12px; 
        font-weight: bold;
    }
    .sentiment-negative { 
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 4px 12px; 
        border-radius: 12px; 
        font-weight: bold;
    }
    .sentiment-neutral { 
        background-color: #fff3cd; 
        color: #856404; 
        padding: 4px 12px; 
        border-radius: 12px; 
        font-weight: bold;
    }
    
    /* Service interest tags - Vanco AI */
    .pref-tag {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 4px 10px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
    }
    
    /* Vanco AI header styling */
    .vanco-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2e7d32 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
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
    """Display chat history with styled messages"""
    history = st.session_state.chat_history.get(customer_id, [])

    if not history:
        st.markdown("""
        <div style='text-align: center; padding: 40px; color: #888;'>
            <h3>👋 Start a Client Conversation</h3>
            <p>Type a message below to begin discussing AI solutions with this enterprise client.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Display messages using Streamlit's chat_message
    for msg in history:
        role = msg.get("role")
        text = msg.get("message")
        timestamp = msg.get("timestamp", "")

        if role == "customer":
            with st.chat_message("user", avatar="👤"):
                st.write(text)
                st.caption(f"🕐 {timestamp}")
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(text)
                st.caption(f"🕐 {timestamp}")


def display_customer_profile(customer_id: str):
    """Display enterprise client profile information"""
    try:
        profile = st.session_state.agent.get_customer_profile(customer_id)
        if not profile:
            st.info("📋 No profile data available for this client yet. Start a conversation to build their profile!")
            return

        # Header Section - Company & Contact Info
        st.markdown("### 🏢 Client Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Company:** {profile.get('company') or '❌ Not identified yet'}")
            st.markdown(f"**Company Type:** {profile.get('company_type') or '❌ Not identified yet'}")
        with col2:
            st.markdown(f"**Industry:** {profile.get('industry') or '❌ Not identified yet'}")
            st.markdown(f"**Email:** {profile.get('email') or '❌ Not provided'}")
        with col3:
            st.markdown(f"**Phone:** {profile.get('phone') or '❌ Not provided'}")
            st.markdown(f"**Budget:** {profile.get('estimated_budget') or '❌ Not discussed'}")

        st.markdown("---")

        # Metrics row - Enterprise focused
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💼 Project Value", f"${profile.get('project_value', profile.get('total_spent', 0)):,.2f}")
        with col2:
            st.metric("💬 Interactions", profile.get('interaction_count', 0))
        with col3:
            sentiment = profile.get('sentiment_trend', 'neutral')
            emoji = "😊" if sentiment == "positive" else "😐" if sentiment == "neutral" else "😞"
            st.metric(f"{emoji} Sentiment", sentiment.capitalize())
        with col4:
            meetings_count = len(profile.get('scheduled_meetings', []))
            st.metric("📅 Meetings", meetings_count)

        st.markdown("---")

        # Scheduled Meetings Section
        st.markdown("### 📅 Scheduled Meetings")
        meetings = profile.get('scheduled_meetings', [])
        if meetings:
            for meeting in meetings:
                st.markdown(f"""
                <div style='background-color: #e8f5e9; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #4caf50;'>
                    <strong>📅 {meeting.get('date', 'TBD')}</strong> at <strong>{meeting.get('time', 'TBD')}</strong><br>
                    <span style='color: #666;'>Purpose: {meeting.get('purpose', 'Project Discussion')}</span><br>
                    <span style='background-color: #c8e6c9; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>{meeting.get('status', 'scheduled').upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No meetings scheduled yet.")

        st.markdown("---")

        # Proposed Projects Section
        st.markdown("### 📋 Proposed Projects")
        proposed = profile.get('proposed_projects', [])
        if proposed:
            for project in proposed:
                value_str = f"${project.get('estimated_value'):,.2f}" if project.get('estimated_value') else "TBD"
                st.markdown(f"""
                <div style='background-color: #fff3e0; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #ff9800;'>
                    <strong>🚀 {project.get('project_name', 'New Project')}</strong> ({project.get('project_type', 'AI Solution')})<br>
                    <span style='color: #666;'>{project.get('description', 'No description')}</span><br>
                    <strong>Estimated Value:</strong> {value_str} | <span style='background-color: #ffe0b2; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>{project.get('status', 'proposed').upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No projects proposed yet. Continue the conversation to identify project opportunities!")

        st.markdown("---")

        # Key Requirements Section
        st.markdown("### ✅ Key Requirements Identified")
        requirements = profile.get('key_requirements', [])
        if requirements:
            for req in requirements:
                st.markdown(f"- ✓ {req}")
        else:
            st.info("No specific requirements captured yet.")

        st.markdown("---")

        # Two column layout for services and issues
        col_left, col_right = st.columns(2)

        with col_left:
            # Service Interests
            st.markdown("### 🏷️ AI/Tech Interests")
            preferences = profile.get('preferences', [])
            if preferences:
                pref_html = " ".join([f'<span class="pref-tag">#{pref}</span>' for pref in preferences])
                st.markdown(pref_html, unsafe_allow_html=True)
            else:
                st.info("No interests detected yet.")

            st.markdown("### 🎯 Service Interests")
            service_interests = profile.get('service_interests', [])
            if service_interests:
                for service in service_interests:
                    st.markdown(f"- 🔹 {service}")
            else:
                st.info("No specific services discussed yet.")

        with col_right:
            # Support Requests
            st.markdown("### ⚠️ Support Requests")
            issues = profile.get('issues_reported', [])
            if issues:
                for issue in issues[-3:]:
                    status = "✅ Resolved" if issue.get('resolved') else "🔴 Open"
                    with st.expander(f"{status} {issue.get('description', '')[:50]}..."):
                        st.write(f"**Description:** {issue.get('description')}")
                        st.write(f"**Category:** {issue.get('category', 'N/A')}")
                        st.write(f"**Severity:** {issue.get('severity', 'N/A')}")
            else:
                st.success("No support requests! 🎉")

        st.markdown("---")

        # Project History (instead of Purchase History)
        st.markdown("### 🚀 Completed AI Projects")
        projects = profile.get('project_history', profile.get('purchase_history', []))
        if projects:
            for project in projects[-5:]:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{project.get('project_name', project.get('product_name', 'N/A'))}**")
                with col2:
                    st.write(f"${project.get('value', project.get('amount', 0)):,.2f}")
                with col3:
                    st.write(f"📁 {project.get('service_category', project.get('category', 'N/A'))}")
        else:
            st.info("No completed projects yet.")

        # Tags Section
        st.markdown("---")
        st.markdown("### 🏷️ Tags")
        tags = profile.get('tags', [])
        if tags:
            tags_html = " ".join([f'<span style="background-color: #e0e0e0; padding: 4px 10px; border-radius: 15px; margin: 2px; font-size: 12px;">{tag}</span>' for tag in tags])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.info("No tags assigned.")

    except Exception as e:
        st.error(f"Error displaying profile: {str(e)}")


def display_memory_history(customer_id: str):
    """Display memory history and interaction details"""
    st.subheader("🧠 Memory & Interaction History")
    
    # Get memories from agent
    memories = st.session_state.agent.get_customer_memories(customer_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Stored Memories")
        if memories:
            for idx, memory in enumerate(memories[-10:], 1):
                memory_type = memory.get('type', 'unknown')
                content = memory.get('content', '')
                metadata = memory.get('metadata', {})
                timestamp = metadata.get('timestamp', '')[:16] if metadata.get('timestamp') else ''
                
                icon = "💬" if memory_type == "customer_query" else "🤖" if memory_type == "agent_response" else "📌"
                
                with st.expander(f"{icon} Memory #{idx} - {memory_type}"):
                    st.write(content)
                    if timestamp:
                        st.caption(f"🕐 {timestamp}")
                    if metadata.get('sentiment'):
                        st.caption(f"Sentiment: {metadata.get('sentiment')}")
        else:
            st.info("No memories stored yet. Start chatting to build memory!")
    
    with col2:
        st.markdown("### 📊 Profile Summary")
        profile_summary = st.session_state.agent.get_profile_summary(customer_id)
        st.text(profile_summary)


def display_recommendations(customer_id: str):
    """Display AI service recommendations"""
    st.subheader("🎯 AI-Powered Service Recommendations")
    
    if st.session_state.agent:
        # Try recommend_services first, fallback to recommend_products for backward compatibility
        try:
            recommendations = st.session_state.agent.profile_builder.recommend_services(customer_id)
        except AttributeError:
            recommendations = st.session_state.agent.profile_builder.recommend_products(customer_id)
        
        if recommendations:
            st.markdown("Based on client's project history and AI/tech interests:")
            st.markdown("---")
            
            cols = st.columns(min(len(recommendations), 3))
            for idx, rec in enumerate(recommendations[:6]):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; 
                                text-align: center; margin: 5px 0; border: 1px solid #90caf9;'>
                        <h4 style='margin: 0; color: #1565c0;'>🚀 {rec}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 No recommendations yet. As the client interacts more, personalized AI service recommendations will appear!")
            
            st.markdown("---")
            st.markdown("### 📈 How to get recommendations:")
            st.markdown("""
            1. **Chat with the client** - discuss their AI needs and challenges
            2. **Add projects** - build their project history  
            3. **Detect interests** - the AI will learn from conversations
            """)


# Main Streamlit App
def main():
    st.title("🚀 VANCO AI - Enterprise Client Relationship Agent")
    st.markdown("*Custom AI Development from Concept to Production | Powered by LangChain, LangGraph & OpenAI*")

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=VANCO+AI", use_container_width=True)
        st.header("⚙️ Configuration")

        if st.button("🚀 Initialize Agent", key="init_btn", use_container_width=True):
            with st.spinner("Initializing agent..."):
                if initialize_agent():
                    st.success("✅ Agent initialized!")
                else:
                    st.error("❌ Failed to initialize")

        if st.session_state.agent is None:
            st.warning("⚠️ Agent not initialized. Click 'Initialize Agent' to start.")
            st.stop()

        # Enterprise Client Management
        st.markdown("---")
        st.subheader("🏢 Enterprise Client Management")

        with st.form("new_customer_form", clear_on_submit=True):
            st.write("**Add New Enterprise Client**")
            cust_id = st.text_input("Client ID", placeholder="client_001")
            cust_name = st.text_input("Contact Name", placeholder="John Smith")
            cust_company = st.text_input("Company Name", placeholder="Acme Corporation")
            cust_industry = st.selectbox("Industry", 
                ["", "Automotive", "Healthcare", "Finance & Banking", "Retail & E-commerce", 
                 "Manufacturing", "Logistics", "Technology", "Energy", "Telecommunications"],
                label_visibility="visible"
            )
            cust_email = st.text_input("Email", placeholder="john@acme.com")
            submitted = st.form_submit_button("➕ Add Client", use_container_width=True)

            if submitted and cust_id and cust_name:
                if add_customer(cust_id, cust_name, cust_email, cust_company, cust_industry):
                    st.success(f"✅ Added {cust_name} from {cust_company}!")

        # Client selection
        st.markdown("---")
        if st.session_state.customers:
            st.write("**Select Enterprise Client**")
            customer_options = {
                f"{info['name']} ({info.get('company', cid)})": cid
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
                
            # Show client count
            st.caption(f"🏢 Enterprise clients: {len(st.session_state.customers)}")
        else:
            st.info("No clients yet. Add an enterprise client to get started!")

    # Main content
    if st.session_state.current_customer is None:
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>👈 Select an enterprise client from the sidebar to begin</h2>
            <p>Or add a new client to start managing AI project relationships!</p>
        </div>
        """, unsafe_allow_html=True)
        return

    customer_id = st.session_state.current_customer
    customer_info = st.session_state.customers.get(customer_id, {})

    # Client header
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f"### 🏢 {customer_info.get('name', 'Unknown')} | {customer_info.get('company', 'N/A')}")
        st.markdown(f"*Industry: `{customer_info.get('industry') or 'N/A'}` | Email: {customer_info.get('email') or 'N/A'}*")
    with col_header2:
        chat_count = len(st.session_state.chat_history.get(customer_id, []))
        st.metric("Messages", chat_count)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "💼 Client Profile", "🧠 AI Memory", "🎯 Service Recommendations"])

    with tab1:
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            display_chat_messages(customer_id)

        st.markdown("---")
        
        # Input section with chat_input for better UX
        user_message = st.chat_input(
            placeholder="Type your message here and press Enter...",
            key="chat_input"
        )
        
        if user_message:
            # Process message directly
            customer_name = customer_info.get('name', 'Customer')
            
            with st.spinner("🤔 Thinking..."):
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
        
        # Quick action buttons
        st.markdown("##### 💡 Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🤖 AI Consulting", use_container_width=True):
                pass  # Use chat_input instead
        with col2:
            if st.button("🚀 New Project", use_container_width=True):
                pass
        with col3:
            if st.button("📅 Schedule Demo", use_container_width=True):
                pass
        with col4:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history[customer_id] = []
                st.rerun()

    with tab2:
        display_customer_profile(customer_id)

    with tab3:
        display_memory_history(customer_id)

    with tab4:
        display_recommendations(customer_id)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px;'>
    <p>🚀 VANCO AI - Enterprise Client Relationship Agent | Custom AI Development from Concept to Production</p>
    <p>Powered by LangChain, LangGraph, OpenAI & Supermemory | Trusted by 50+ Enterprises</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

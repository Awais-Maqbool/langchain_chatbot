import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Color Palette
# Primary: Deep Navy #1e3a5f
# Secondary: Steel Blue #334155
# Accent: Electric Blue #3b82f6
# Background: Dark Slate #0f172a
# Surface: Slate #1e293b
# Text: Light Gray #e2e8f0

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main background - Professional dark theme */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        min-height: 100vh;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 50%, #1e3a5f 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .header-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }

    .header-subtitle {
        font-size: 1rem !important;
        color: #94a3b8 !important;
        margin-top: 0.5rem !important;
        font-weight: 400;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(59, 130, 246, 0.1);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    .sidebar-header {
        color: #f8fafc !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding: 1rem 0;
        border-bottom: 2px solid #3b82f6;
        margin-bottom: 1.5rem;
        letter-spacing: -0.3px;
    }

    /* Sidebar sections */
    .sidebar-section {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }

    .sidebar-section-title {
        color: #94a3b8 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }

    /* Chat message containers */
    .chat-message {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin-bottom: 0.75rem;
        animation: fadeIn 0.3s ease-in-out;
        line-height: 1.6;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: #ffffff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .assistant-message {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border-bottom-left-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.1);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        padding: 0.875rem 1.25rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        outline: none;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: -0.2px;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%) !important;
    }

    /* Chat container styling */
    .chat-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 1.25rem;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(59, 130, 246, 0.1);
    }

    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 64, 175, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(59, 130, 246, 0.2);
        text-align: center;
    }

    .stat-value {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #60a5fa !important;
    }

    .stat-label {
        font-size: 0.8rem !important;
        color: #94a3b8 !important;
        font-weight: 500;
    }

    /* Info boxes */
    .stInfo {
        background: rgba(30, 64, 175, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    .stInfo > div {
        color: #e2e8f0 !important;
    }

    /* Warning banner */
    .warning-banner {
        background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 500;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.85; }
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #64748b;
        font-size: 0.8rem;
        border-top: 1px solid rgba(59, 130, 246, 0.1);
        margin-top: 2rem;
    }

    .footer a {
        color: #3b82f6;
        text-decoration: none;
    }

    /* Divider */
    .custom-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.2), transparent);
        margin: 1.25rem 0;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1e293b;
    }

    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #60a5fa;
    }

    /* Chat input container */
    .stChatInputContainer {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="gemma:2b",
        temperature=0,
    )

# Create prompt and chain
@st.cache_resource
def get_chain():
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'max_turns' not in st.session_state:
    st.session_state.max_turns = 5

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Settings</div>', unsafe_allow_html=True)

    # Model info
    st.markdown("### 🤖 Model Configuration")
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.info(f"**Model:** gemma:2b")
    st.info(f"**Temperature:** 0")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Session stats
    st.markdown("### 📊 Session Stats")
    current_turns = len(st.session_state.chat_history) // 2

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{current_turns}</div>
            <div class="stat-label">Turns</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        remaining = st.session_state.max_turns - current_turns
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{remaining}</div>
            <div class="stat-label">Remaining</div>
        </div>
        """, unsafe_allow_html=True)

    # Progress bar
    progress = current_turns / st.session_state.max_turns
    st.progress(progress)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Actions
    st.markdown("### 🎯 Actions")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Info
    st.markdown("### ℹ️ About")
    st.markdown("""
    **AI Chat Assistant**

    Built with **LangChain** and **Ollama** for intelligent conversations.

    ---

    **Features:**
    - 🤖 Gemma 2B model
    - 💬 Context-aware chat
    - 🔄 Conversation history
    """)

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">💬 AI Chat Assistant</h1>
    <p class="header-subtitle">Intelligent conversations powered by LangChain & Ollama</p>
</div>
""", unsafe_allow_html=True)

# Warning banner
current_turns = len(st.session_state.chat_history) // 2
remaining = st.session_state.max_turns - current_turns
if remaining <= 2 and remaining > 0:
    st.markdown(f"""
    <div class="warning-banner">
        ⚠️ Warning: Only {remaining} turn(s) remaining! Type "clear" to start fresh.
    </div>
    """, unsafe_allow_html=True)
elif remaining <= 0:
    st.markdown("""
    <div class="warning-banner">
        🚫 Context window is full! The AI may not follow properly. Please clear the chat.
    </div>
    """, unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="chat-message user-message">{message.content}</div>', unsafe_allow_html=True)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f'<div class="chat-message assistant-message">{message.content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if current_turns < st.session_state.max_turns:
    if prompt := st.chat_input("Type your message here...", key="chat_input"):
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=prompt))

        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)

        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    chain = get_chain()
                    response = chain.invoke({
                        'question': prompt,
                        'chat_history': st.session_state.chat_history[:-1]
                    })
                    st.session_state.chat_history.append(AIMessage(content=response))
                    st.markdown(f'<div class="chat-message assistant-message">{response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state.chat_history.pop()
else:
    st.markdown("""
    <div class="warning-banner">
        🚫 Maximum conversation limit reached! Please clear the chat to continue.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🤖 AI Chat Assistant | Built with Streamlit & LangChain</p>
    <p>Powered by Ollama | Model: gemma:2b</p>
</div>
""", unsafe_allow_html=True)

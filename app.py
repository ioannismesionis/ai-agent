"""
Career Advisor AI - Streamlit UI
Interactive interface for career transition guidance
"""

import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import ADK components
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, preload_memory
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

# Page configuration
st.set_page_config(
    page_title="Career Advisor AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-output {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .agent-name {
        font-weight: bold;
        color: #1f77b4;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_service' not in st.session_state:
    st.session_state.session_service = InMemorySessionService()
if 'memory_service' not in st.session_state:
    st.session_state.memory_service = InMemoryMemoryService()
if 'runner' not in st.session_state:
    st.session_state.runner = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = "streamlit_session"

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Memory callback
async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    try:
        agent_name = callback_context._invocation_context.agent.name
        session = callback_context._invocation_context.session
        await callback_context._invocation_context.memory_service.add_session_to_memory(session)
    except Exception as e:
        st.warning(f"Memory save failed: {e}")

@st.cache_resource
def initialize_agent():
    """Initialize the agent and runner (cached)."""

    # Research Agent
    research_agent = LlmAgent(
        name="research_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
        You are a Research Agent specialized in career transitions.

        Your task:
        1. Extract career transition details from the user's message or check preload_memory for context
        2. Use the Google Search tool to research the target career path
        3. Focus on: required skills, typical career progression, salary ranges, and job market demand
        4. Search for: online courses, certifications, and learning resources
        5. Look for: success stories of people who made similar transitions

        Output format:
        ## Key Skills Required
        [List 5-7 essential skills with brief descriptions]

        ## Learning Resources
        [Specific courses, certifications, books, and platforms]

        ## Market Outlook
        [Job demand, salary ranges, growth trends with data]

        ## Transition Timeline
        [Typical timeframe for this transition based on the user's experience level]

        ## Success Stories
        [Brief examples of successful transitions]

        Keep your research comprehensive but concise. Focus on actionable information tailored to the user's background.
        """,
        tools=[google_search, preload_memory],
        output_key="research_summary",
        after_agent_callback=auto_save_to_memory,
    )

    # Mentor Agent
    mentor_agent = LlmAgent(
        name="mentor_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""
        You are a Career Mentor Agent. Based on the research findings: {research_summary}

        Extract the user's context from the conversation history and research summary, then create a personalized, actionable transition plan.

        Structure your plan as follows:

        ## Phase 1: Foundation (Months 1-3)
        - Specific skills to learn first (prioritized based on their background)
        - Recommended courses/resources with links when available
        - Daily/weekly time commitment suggestions
        - Quick wins to build confidence

        ## Phase 2: Building Portfolio (Months 4-6)
        - Concrete projects to build (with examples relevant to their experience)
        - GitHub repositories to create
        - Communities to join (specific names)
        - Networking strategies leveraging their current role

        ## Phase 3: Job Search (Months 6-9)
        - Resume updates needed (specific sections)
        - Where to apply (companies, job boards)
        - Interview preparation tips
        - Portfolio presentation strategies

        ## Milestones & Checkpoints
        - Monthly goals with measurable outcomes
        - How to measure progress
        - Red flags and when to adjust course

        ## Leveraging Your Background
        - How to translate their existing skills to the new role
        - Unique advantages from their current position
        - How their experience is an asset

        Make it specific, realistic, and encouraging. Use actual course names, platforms, and communities when possible.
        Keep the tone supportive but practical - acknowledge challenges while emphasizing achievability.
        Tailor everything to their specific situation.
        """,
        output_key="career_advice",
    )

    # Root Agent
    root_agent = SequentialAgent(
        name="CareerPathPipeline",
        sub_agents=[research_agent, mentor_agent],
    )

    return root_agent

async def run_agent(user_query, show_all_agents=True):
    """Run the agent and collect responses."""

    # Get or create runner
    if st.session_state.runner is None:
        root_agent = initialize_agent()
        st.session_state.runner = Runner(
            agent=root_agent,
            app_name="career_advisor_app",
            session_service=st.session_state.session_service,
            memory_service=st.session_state.memory_service,
        )

    runner = st.session_state.runner

    # Create or retrieve session
    try:
        session = await st.session_state.session_service.create_session(
            app_name="career_advisor_app",
            user_id="streamlit_user",
            session_id=st.session_state.session_id
        )
    except:
        session = await st.session_state.session_service.get_session(
            app_name="career_advisor_app",
            user_id="streamlit_user",
            session_id=st.session_state.session_id
        )

    # Convert query to Content
    query_content = types.Content(role="user", parts=[types.Part(text=user_query)])

    # Collect responses
    responses = []

    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=query_content
    ):
        if event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                agent_name = getattr(event, 'author', 'Agent')
                responses.append({
                    'agent': agent_name,
                    'text': text
                })

    return responses

# Header
st.markdown('<div class="main-header">🎯 Career Advisor AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Personalized guidance for your career transition</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    show_research = st.checkbox("Show Research Output", value=True, help="Display detailed research findings")
    show_mentor = st.checkbox("Show Mentor Plan", value=True, help="Display the personalized action plan")

    st.divider()

    st.header("💡 How to Use")
    st.markdown("""
    1. **Describe your situation** in the text area below
    2. Include:
       - Current role
       - Years of experience
       - Target role
       - Available time per week
    3. Click **Get Career Advice**
    4. Review the research and personalized plan

    **Example:**
    > "I'm a Product Manager with 5 years of experience. I want to transition to Data Science and can dedicate 10 hours per week."
    """)

    st.divider()

    if st.button("🔄 New Session", help="Start a fresh conversation"):
        st.session_state.conversation_history = []
        st.session_state.session_id = f"session_{len(st.session_state.conversation_history)}"
        st.rerun()

# Main content
st.header("📝 Your Career Transition Query")

user_input = st.text_area(
    "Tell me about your career transition goals:",
    height=150,
    placeholder="Example: I am a Product Manager with 5 years of experience. I want to transition to data science and can dedicate 10 hours per week.",
    help="Provide as much detail as possible for better personalized advice"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button("🚀 Get Career Advice", type="primary", use_container_width=True)

if submit_button and user_input:
    # Add to conversation history
    st.session_state.conversation_history.append({
        'role': 'user',
        'content': user_input
    })

    # Show processing
    with st.spinner("🔍 Researching career transition paths..."):
        try:
            # Run the agent
            responses = asyncio.run(run_agent(user_input, show_all_agents=True))

            # Display responses
            st.success("✅ Analysis Complete!")

            for response in responses:
                agent_name = response['agent']
                text = response['text']

                # Show research output
                if agent_name == 'research_agent' and show_research:
                    with st.expander("🔬 Research Findings", expanded=True):
                        st.markdown(text)

                # Show mentor output
                elif agent_name == 'mentor_agent' and show_mentor:
                    with st.expander("🎓 Personalized Career Plan", expanded=True):
                        st.markdown(text)

            # Add to conversation history
            st.session_state.conversation_history.append({
                'role': 'assistant',
                'content': responses
            })

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

elif submit_button and not user_input:
    st.warning("⚠️ Please enter your career transition query above.")

# Display conversation history
if st.session_state.conversation_history:
    st.divider()
    st.header("💬 Conversation History")

    for i, msg in enumerate(st.session_state.conversation_history):
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.write(msg['content'])
        else:
            with st.chat_message("assistant"):
                st.write("Career Advisor Response")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built with ❤️ using Google ADK and Streamlit</p>
    <p style='font-size: 0.8rem;'>Powered by Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)

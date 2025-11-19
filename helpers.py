"""
Helper functions and utilities for the AI Career Advisor agent.

This module contains:
- Configuration (retry settings, constants)
- Session management utilities
- Memory callbacks
- Display helpers
"""

from google.adk.runners import Runner
from google.genai import types


# ============================================================================
# Configuration
# ============================================================================

# Application constants
APP_NAME = "career_advisor"
USER_ID = "default"
MODEL_NAME = "gemini-2.5-flash-lite"

# Retry configuration for API calls
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Exponential backoff multiplier
    initial_delay=1,  # Initial delay in seconds
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


# ============================================================================
# Memory Callbacks
# ============================================================================

async def auto_save_to_memory(callback_context):
    """
    Automatically save session to memory after each agent turn.

    This callback:
    - Extracts the agent name and session from the callback context
    - Saves the session to memory service
    - Logs success or failure
    - Fails gracefully without breaking the agent flow

    Args:
        callback_context: The callback context provided by ADK
    """
    try:
        agent_name = callback_context._invocation_context.agent.name
        session = callback_context._invocation_context.session

        await callback_context._invocation_context.memory_service.add_session_to_memory(session)

        print(f"💾 Saved {agent_name} output to memory")
    except Exception as e:
        print(f"⚠️  Warning: Failed to save to memory: {e}")
        # Don't raise - let the agent continue even if memory save fails


# ============================================================================
# Session Management
# ============================================================================

async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
    last_agent_only: bool = False,
):
    """
    Run queries in a session and display agent responses.

    This function:
    - Creates or retrieves a session
    - Processes user queries sequentially
    - Streams agent responses
    - Optionally shows all agents or just the final output

    Args:
        runner_instance: The ADK Runner instance
        user_queries: Single query string or list of queries
        session_name: Session ID for conversation tracking
        last_agent_only: If True, only show the final agent's output

    Example:
        await run_session(
            runner,
            "I want to transition from PM to Data Science",
            session_name="my-session",
            last_agent_only=True
        )
    """
    print(f"\n{'='*60}")
    print(f"Session: {session_name}")
    print(f"{'='*60}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Import here to avoid circular dependency
    from google.genai import types

    # Get session service from runner's invocation context
    # We'll need to access it through the runner
    session_service = runner_instance._session_service

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
        print("✅ New session created")
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
        print("✅ Existing session retrieved")

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\n👤 User: {query}")
            print(f"{'-'*60}")

            # Convert the query string to the ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            responses = []  # Buffer to collect responses with agent names

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query_content
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    text = event.content.parts[0].text
                    if text and text != "None":
                        # Get agent name from author attribute
                        agent_name = getattr(event, 'author', 'Unknown Agent')

                        if last_agent_only:
                            # Collect all responses with agent names
                            responses.append({
                                'agent': agent_name,
                                'text': text
                            })
                        else:
                            # Print all responses in real-time
                            print(f"\n🤖 {agent_name}:")
                            print(text)

            # Print only the last response if filtering
            if last_agent_only and responses:
                last_response = responses[-1]
                print(f"\n🤖 {last_response['agent']} (Final):")
                print(last_response['text'])
    else:
        print("⚠️  No queries provided!")

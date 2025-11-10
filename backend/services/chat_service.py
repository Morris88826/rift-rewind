"""
Chat service that integrates with the Bedrock League Analytics Agent.
"""
from services.bedrock_agent import get_agent_response


def get_chat_response(user_message: str, puuid: str = None) -> str:
    """
    Get a response from the Bedrock League Analytics Agent.

    Args:
        user_message: The user's message to the agent
        puuid: Optional player PUUID for personalized context

    Returns:
        The agent's response as a string
    """
    try:
        response = get_agent_response(user_message, puuid)
        return response
    except Exception as e:
        raise Exception(f"Error getting chat response: {str(e)}")

"""
Bedrock AI Agent with Knowledge Base access for League of Legends analytics.
Uses S3-backed Knowledge Base (same approach as league_analytics_agent.py).
"""
import os
import json
from dotenv import load_dotenv

try:
    from strands import Agent, tool
    from strands.models import BedrockModel
    import boto3
except ImportError:
    raise ImportError(
        "Bedrock agent dependencies not installed. "
        "Install with: pip install strands boto3"
    )

# Load environment variables
load_dotenv()

# Configuration from .env
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "229CDNHRIX")
MODEL_ARN = os.getenv("MODEL_ARN", "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0")
AGENT_MODEL_ID = os.getenv("AGENT_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0")

# Initialize Bedrock clients
bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)

bedrock_model = BedrockModel(
    model_id=AGENT_MODEL_ID,
    region_name=REGION,
)

# =====================================================================
# KNOWLEDGE BASE QUERY TOOL (similar to chatbot example)
# =====================================================================

@tool
def query_match_data(query: str, max_results: int = 5) -> str:
    """
    Query the Bedrock Knowledge Base for League of Legends match/performance data.
    """
    if KNOWLEDGE_BASE_ID == "YOUR_KB_ID_HERE":
        return "Knowledge base is not configured. Please set KNOWLEDGE_BASE_ID in the .env file."
    if not MODEL_ARN.startswith("arn:aws:bedrock"):
        return "RAG model ARN is not configured. Please set MODEL_ARN in the .env file."

    try:
        resp = bedrock_runtime.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": MODEL_ARN,
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": max_results
                        }
                    }
                }
            }
        )

        answer = resp.get("output", {}).get("text", "")
        citations = resp.get("citations", [])
        num_sources = len(citations)

        return f"{answer}\n\nSources used: {num_sources}"

    except Exception as e:
        return f"Error querying knowledge base: {e}"


@tool
def analyze_player_performance(player_name: str, stat_type: str = None) -> str:
    """
    Analyze a player's League of Legends performance from the knowledge base.
    stat_type can be: KDA, win_rate, champion_stats, role_stats, etc.
    """
    parts = [f"player performance analysis for {player_name}"]
    if stat_type:
        parts.append(f"focusing on {stat_type}")
    parts.append("include detailed statistics")
    q = " ".join(parts)
    return query_match_data(q, max_results=8)


@tool
def analyze_meta_trends(patch_version: str = None, time_period: str = "last 30 days") -> str:
    """
    Analyze current League of Legends meta trends and champion performance.
    """
    parts = ["meta trends analysis"]
    if patch_version:
        parts.append(f"in patch {patch_version}")
    else:
        parts.append(f"over the {time_period}")
    parts.append("include popular champions, item builds, and playstyle shifts")
    q = " ".join(parts)
    return query_match_data(q, max_results=10)


@tool
def compare_champions(champion1: str, champion2: str) -> str:
    """
    Compare two League of Legends champions in the current meta.
    """
    q = (
        f"Compare {champion1} and {champion2} in League of Legends. "
        "Include win rates, pick rates, matchups, strengths, and weaknesses."
    )
    return query_match_data(q, max_results=12)


# =====================================================================
# AGENT DEFINITION
# =====================================================================

agent = Agent(
    model=bedrock_model,
    system_prompt=(
        "You are a League of Legends analytics expert. "
        "When users ask for specific, data-backed information about players, champions, or meta, "
        "use the available tools to query the knowledge base. "
        "Provide detailed analysis based on the retrieved data. "
        "If the knowledge base doesn't have the requested information, be transparent about it."
    ),
    tools=[
        query_match_data,
        analyze_player_performance,
        analyze_meta_trends,
        compare_champions,
    ],
)


def get_agent_response(message: str, puuid: str = None) -> str:
    """
    Get a response from the Bedrock agent using Knowledge Base.

    Args:
        message: User's message
        puuid: Optional player PUUID for context (can be included in the message)

    Returns:
        Agent's response
    """
    try:
        # If puuid is provided, add it as context to the message
        if puuid:
            message = f"[Player PUUID: {puuid}] {message}"

        response = agent(message)

        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)

        return response

    except Exception as e:
        raise Exception(f"Error getting agent response: {str(e)}")

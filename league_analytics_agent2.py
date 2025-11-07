import boto3
from strands import Agent, tool
from strands.models import BedrockModel

# ---------------------------------------------------------------------
# CONFIG: update these with your real values
# ---------------------------------------------------------------------
REGION = "us-east-1"

# From your Bedrock Knowledge Base
KNOWLEDGE_BASE_ID = "229CDNHRIX"  # <- replace if yours is different

# This is the model ARN used by the Knowledge Base for RAG
# Example for Claude 3 Sonnet in us-east-1:
MODEL_ARN = (
    "arn:aws:bedrock:us-east-1::foundation-model/"
    "anthropic.claude-3-haiku-20240307-v1:0"
)


# This is the Bedrock model your agent itself will use to chat
# (this is a model ID, *not* an ARN)
AGENT_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

# ---------------------------------------------------------------------
# AWS CLIENTS
# ---------------------------------------------------------------------
bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)

bedrock_model = BedrockModel(
    model_id=AGENT_MODEL_ID,
    region_name=REGION,
)

# ---------------------------------------------------------------------
# TOOL: query Knowledge Base directly
# ---------------------------------------------------------------------
@tool
def query_match_data(query: str, max_results: int = 5) -> str:
    """
    Query the Bedrock Knowledge Base for League of Legends match/meta data.

    Args:
        query: Natural language question about match data, champions, or meta.
        max_results: Number of KB chunks to retrieve.

    Returns:
        A text answer plus how many KB sources were used.
    """
    if not KNOWLEDGE_BASE_ID:
        return "Knowledge base is not configured. Please set KNOWLEDGE_BASE_ID in the script."
    if not MODEL_ARN.startswith("arn:aws:bedrock"):
        return "RAG modelArn is not configured correctly. Please set MODEL_ARN in the script."

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
                    },
                },
            },
        )

        answer = resp.get("output", {}).get("text", "")
        citations = resp.get("citations", []) or []
        num_sources = sum(
            len(c.get("retrievedReferences", [])) for c in citations
        )

        return f"{answer}\n\nSources used: {num_sources}"

    except Exception as e:
        return f"Error querying knowledge base: {e}"

# ---------------------------------------------------------------------
# EXTRA ANALYSIS TOOLS
# ---------------------------------------------------------------------
@tool
def analyze_champion_performance(
    champion_name: str,
    role: str | None = None,
    rank_tier: str | None = None,
) -> str:
    """
    High-level performance breakdown for a specific champion.
    """
    parts = [f"champion performance analysis for {champion_name}"]
    if role:
        parts.append(f"in the {role} role")
    if rank_tier:
        parts.append(f"in {rank_tier} ranked games")

    parts.append(
        "including win rate, pick rate, ban rate, KDA, and common item builds."
    )

    query = " ".join(parts)
    return query_match_data(query, max_results=8)


@tool
def analyze_meta_trends(
    patch_version: str | None = None,
    time_period: str = "last 30 days",
) -> str:
    """
    Look at overall meta trends, especially around ADCs or specific roles.
    """
    parts = ["meta trends analysis"]

    if patch_version:
        parts.append(f"for patch {patch_version}")
    else:
        parts.append(f"over the {time_period}")

    parts.append(
        "including rising and falling champions, item build shifts, "
        "role strength changes, and key win rate changes."
    )

    query = " ".join(parts)
    return query_match_data(query, max_results=10)


@tool
def compare_team_compositions(
    comp1_description: str,
    comp2_description: str,
) -> str:
    """
    Compare two team comps: strengths, weaknesses, and win conditions.
    """
    query = f"""
    Compare these two League of Legends team compositions.

    Composition 1: {comp1_description}
    Composition 2: {comp2_description}

    Focus on:
    - Engage and peel
    - Scaling
    - Objective control
    - Teamfight strength
    - Draft flexibility and counterpicks
    """

    return query_match_data(query, max_results=12)

# ---------------------------------------------------------------------
# AGENT (no memory, no on_message handlers)
# ---------------------------------------------------------------------
agent = Agent(
    model=bedrock_model,
    system_prompt=(
        "You are a League of Legends analytics expert. "
        "Use the available tools to pull data-backed insights from the "
        "knowledge base when the user asks about statistics, match data, "
        "or meta analysis. Explain your reasoning clearly in plain language."
    ),
    tools=[
        query_match_data,
        analyze_champion_performance,
        analyze_meta_trends,
        compare_team_compositions,
    ],
)

# ---------------------------------------------------------------------
# MAIN: simple one-shot test
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Example test query – you can change this
    user_question = "What are the best Junglers to play right now?"
    response = agent(user_question)


import json
import boto3

from strands import Agent, tool
from strands.models import BedrockModel

# ---------------------------------------------------------------------
# CONFIG: fill these in
# ---------------------------------------------------------------------
REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "229CDNHRIX"  # e.g. "229CDNHRIX"
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"

# this is the model the agent itself will use to talk/reason
AGENT_MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# ---------------------------------------------------------------------
# CLIENTS
# ---------------------------------------------------------------------
bedrock_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)

bedrock_model = BedrockModel(
    model_id=AGENT_MODEL_ID,
    region_name=REGION,
)

# ---------------------------------------------------------------------
# TOOL: query KB directly
# ---------------------------------------------------------------------
@tool
def query_match_data(query: str, max_results: int = 5) -> str:
    """
    Query the Bedrock Knowledge Base for League of Legends match/meta data.
    """
    if KNOWLEDGE_BASE_ID == "YOUR_KB_ID_HERE":
        return "Knowledge base is not configured. Please set KNOWLEDGE_BASE_ID in the script."
    if not MODEL_ARN.startswith("arn:aws:bedrock"):
        return "RAG model ARN is not configured. Please set MODEL_ARN in the script."

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

# ---------------------------------------------------------------------
# EXTRA TOOLS
# ---------------------------------------------------------------------
@tool
def analyze_champion_performance(champion_name: str, role: str = None, rank_tier: str = None) -> str:
    parts = [f"champion performance analysis for {champion_name}"]
    if role:
        parts.append(f"in the {role} role")
    if rank_tier:
        parts.append(f"in {rank_tier} ranked games")
    parts.append("include win rate, pick/ban rate, KDA, and item build success")
    q = " ".join(parts)
    return query_match_data(q, max_results=8)


@tool
def analyze_meta_trends(patch_version: str = None, time_period: str = "last 30 days") -> str:
    parts = ["meta trends for ADC champions"]
    if patch_version:
        parts.append(f"in patch {patch_version}")
    else:
        parts.append(f"over the {time_period}")
    parts.append("include rising champs, falling champs, and build shifts")
    q = " ".join(parts)
    return query_match_data(q, max_results=10)


@tool
def compare_team_compositions(comp1_description: str, comp2_description: str) -> str:
    q = (
        "Compare these two League of Legends team compositions. "
        f"Comp 1: {comp1_description}. "
        f"Comp 2: {comp2_description}. "
        "Include objective control, teamfighting, engage, peel, and scaling."
    )
    return query_match_data(q, max_results=12)

# ---------------------------------------------------------------------
# AGENT
# ---------------------------------------------------------------------
agent = Agent(
    model=bedrock_model,
    system_prompt=(
        "You are a League of Legends analytics expert. "
        "When the user asks for specific, data-backed info, call the tools. "
        "If the knowledge base is not configured or returns no data, say so."
    ),
    tools=[
        query_match_data,
        analyze_champion_performance,
        analyze_meta_trends,
        compare_team_compositions,
    ],
)

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
if __name__ == "__main__":
    agent("What are the best ADCs to play?")


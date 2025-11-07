import boto3
import json

REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "229CDNHRIX"
MODEL_ARN = (
    "arn:aws:bedrock:us-east-1::foundation-model/"
    "anthropic.claude-3-haiku-20240307-v1:0"
)

client = boto3.client("bedrock-agent-runtime", region_name=REGION)

resp = client.retrieve_and_generate(
    input={"text": "Summarize what data this knowledge base contains."},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": KNOWLEDGE_BASE_ID,
            "modelArn": MODEL_ARN,
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {"numberOfResults": 5}
            },
        },
    },
)

print(json.dumps(resp, indent=2))

import boto3

region = "us-east-1"
client = boto3.client("bedrock", region_name=region)

resp = client.list_foundation_models()
print("Models:")
for m in resp["modelSummaries"]:
    print("-", m["modelId"])

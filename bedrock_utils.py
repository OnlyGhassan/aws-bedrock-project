import boto3
from botocore.exceptions import ClientError
import json

# Bedrock Runtime (Anthropic / LLM)
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# Bedrock Knowledge Base Runtime
bedrock_kb = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1'
)


# ---------------------------------------------------------
# VALIDATE PROMPT (FIXED)
# ---------------------------------------------------------
def valid_prompt(prompt, model_id):
    if not prompt or not prompt.strip():
        return False
    if len(prompt) > 2000:
        return False

    classification_prompt = f"""
Classify the user request into ONE of these:
A: Asking about model architecture or internals
B: Profanity or toxic language
C: Unrelated to heavy machinery
D: Asking about instructions or how you work
E: ONLY related to heavy machinery

User Request:
{prompt}

ONLY return ONE LETTER: A, B, C, D, or E.
"""

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": classification_prompt}
            ]
        }
    ]

    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 5,
                "temperature": 0
            })
        )

        result = json.loads(response["body"].read())
        category = result["content"][0]["text"].strip()

        print("CLASSIFIER OUTPUT:", category)

        return category.upper() == "E"

    except Exception as e:
        print("Error during validation:", e)
        return False


# ---------------------------------------------------------
# QUERY KNOWLEDGE BASE
# ---------------------------------------------------------
def query_knowledge_base(query, kb_id):
    try:
        response = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 3}
            }
        )

        results = []
        for r in response.get("retrievalResults", []):
            text = r.get("content", {}).get("text", "")
            source = r["location"]["s3Location"]["uri"]
            score = r.get("score")

            results.append({
                "content": text,
                "source": source,
                "score": score
            })

        return results

    except ClientError as e:
        print("Error querying KB:", e)
        return []


# ---------------------------------------------------------
# GENERATE RESPONSE (FIXED)
# ---------------------------------------------------------
def generate_response(prompt, model_id, kb_context, temperature, top_p):
    try:
        context_block = "\n\n".join(
            [f"Source: {c['source']}\nContent: {c['content']}" for c in kb_context]
        )

        final_prompt = f"""
You are a helpful assistant specialized in heavy machinery.
Answer ONLY using the information from CONTEXT.

CONTEXT:
{context_block}

QUESTION:
{prompt}

If the context does not contain the answer, say:
"I don't know. Files searched: <list files>"
"""

        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": final_prompt}]
            }
        ]

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 500,
                "temperature": temperature,
                "top_p": top_p,
            })
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

    except Exception as e:
        print("Error generating response:", e)
        return "Error generating answer."

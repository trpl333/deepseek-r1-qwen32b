import runpod
import requests
import json
import os

# vLLM API URL inside the same container
VLLM_URL = "http://localhost:8000/v1/completions"   # Default port for vLLM OpenAI server

def handler(event):
    """
    RunPod Serverless handler.
    Expects:
    {
        "prompt": "your text",
        "max_tokens": 200
    }
    """

    prompt = event.get("prompt", "")
    max_tokens = event.get("max_tokens", 200)

    payload = {
        "model": os.getenv("MODEL_PATH", "/workspace"),
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(VLLM_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data

    except Exception as e:
        return {"error": str(e)}

# Start the RunPod serverless loop
runpod.serverless.start({"handler": handler})

FROM runpod/worker-vllm:v2.11.0

# Copy model weights into /workspace (RunPod clones your repo here)
WORKDIR /workspace

# Environment variables for vLLM
ENV MODEL_PATH=/workspace

# Start vLLM
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", 
     "--model", "/workspace",
     "--trust-remote-code",
     "--dtype", "auto",
     "--tensor-parallel-size", "1",
     "--max-model-len", "32768"]

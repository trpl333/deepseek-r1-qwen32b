FROM runpod/worker-vllm:v2.11.0

WORKDIR /workspace
ENV MODEL_PATH=/workspace

CMD ["python3", "-m", "vllm.entrypoints.openai.api_server",
     "--model", "/workspace",
     "--trust-remote-code",
     "--dtype", "auto",
     "--tensor-parallel-size", "1",
     "--max-model-len", "32768"]

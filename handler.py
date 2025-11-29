import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Use MODEL_PATH from environment (set in .runpod/hub.json presets)
MODEL_NAME = os.environ.get("MODEL_PATH", "/workspace")

_tokenizer = None
_model = None

def _load_model_once():
    global _tokenizer, _model
    if _model is None or _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

def handler(event):
    # Lazy load on first call to avoid failing at import time
    try:
        _load_model_once()
    except Exception as e:
        # Return a friendly message so test runner doesn't crash hard
        return {"output": f"model load failed: {e}"}

    prompt = event.get("input", {}).get("prompt", "")
    max_tokens = event.get("input", {}).get("max_tokens", 200)

    inputs = _tokenizer(prompt, return_tensors="pt").to(_model.device)
    output_ids = _model.generate(
        **inputs,
        max_length=max_tokens,
        do_sample=True,
        temperature=0.2
    )
    result = _tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return {"output": result}

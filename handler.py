import runpod
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model globally so it stays warm between invocations
MODEL_NAME = "/workspace"   # your GitHub-cloned model folder

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

def handler(event):
    prompt = event["input"].get("prompt", "")
    max_tokens = event["input"].get("max_tokens", 200)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_length=max_tokens,
        do_sample=True,
        temperature=0.2
    )

    result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return { "output": result }

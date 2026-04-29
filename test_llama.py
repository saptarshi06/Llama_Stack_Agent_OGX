# test_llama.py
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="http://localhost:8321")

print("Testing Llama Stack connection...")

# Test 1: List models
try:
    models = client.models.list()
    print(f"✓ Models found: {[m.identifier for m in models]}")
except Exception as e:
    print(f"✗ Failed to list models: {e}")

# Test 2: Try inference
try:
    response = client.inference.chat_completion(
        model_id="ollama/llama3.2:3b",
        messages=[{"role": "user", "content": "Say hello"}],
        stream=False
    )
    print(f"✓ Response: {response.completion_message.content}")
except Exception as e:
    print(f"✗ Inference failed: {e}")
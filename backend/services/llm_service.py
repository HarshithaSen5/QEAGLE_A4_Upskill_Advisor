# llm_service.py
"""
Service for interacting with a local Ollama LLM (e.g., Mistral, Llama2) via REST API.
"""
import requests

class LLMService:
    def __init__(self, model_name="phi3", endpoint="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint
        print(f"[LLMService] Using Ollama model: {self.model_name}")
        print(f"[LLMService] Using endpoint: {self.endpoint}")

    def generate(self, prompt, context=None):
        # Combine context and prompt if context is provided
        full_prompt = f"{context}\n{prompt}" if context else prompt
        data = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }
        print(f"[LLMService] Sending request to Ollama...")
        print(f"[LLMService] Data: {data}")
        try:
            response = requests.post(self.endpoint, json=data, timeout=120)  # Increased timeout to 120 seconds
            print(f"[LLMService] Response status: {response.status_code}")
            print(f"[LLMService] Response body: {response.text}")
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            print(f"[LLMService] ERROR: {e}")
            return None
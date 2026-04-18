from guardrail_gym.models.factory import get_model_adapter

MODELS = [
    "gpt-4.1",
    "gemini-2.5-flash",
    "claude-sonnet-4-5",
    "Qwen/Qwen3.5-27B",
    "google/gemma-4-27b-it",
    "mistralai/Ministral-3B-Instruct",
    "nvidia/Nemotron-3-Nano-30B-A3B",
    "mock-llm",
]

def main():
    for model_name in MODELS:
        adapter = get_model_adapter(model_name)
        print(model_name, "->", adapter.__class__.__name__)

if __name__ == "__main__":
    main()

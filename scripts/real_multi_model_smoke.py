from __future__ import annotations

from guardrail_gym.models.factory import get_model_adapter

MODELS = [
    "gpt-4.1",
    "gemini-2.5-flash",
    "claude-sonnet-4-5",
]

def main():
    for model_name in MODELS:
        print("=" * 80)
        print("testing:", model_name)
        adapter = get_model_adapter(model_name)
        try:
            resp = adapter.generate(
                prompt="Say hello in one short sentence.",
                system_prompt="Be concise.",
            )
            print("adapter:", adapter.__class__.__name__)
            print("latency_ms:", resp.latency_ms)
            print("text:", resp.text[:200])
        except Exception as e:
            print("skipped:", type(e).__name__, str(e))

if __name__ == "__main__":
    main()

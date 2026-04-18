from __future__ import annotations

from guardrail_gym.models.factory import get_model_adapter


def main():
    adapter = get_model_adapter("gpt-4.1")
    resp = adapter.generate("Say hello in one sentence.", system_prompt="Be concise.")
    print("model:", resp.model_name)
    print("latency_ms:", resp.latency_ms)
    print("text:", resp.text)


if __name__ == "__main__":
    main()

from guardrail_gym.benchmark.spec import BenchmarkSpec
from guardrail_gym.evoguard.search import EvoGuardSearch
from guardrail_gym.profiles.recommend import GuardrailRecommender
from guardrail_gym.profiles.schemas import ComplianceProfile


def test_profile_recommendation_smoke() -> None:
    profile = ComplianceProfile(
        domain="healthcare",
        jurisdiction=["US"],
        user_vulnerability="high",
        data_sensitivity="phi",
        autonomy="advisory",
        actionability="decision_adjacent",
        model_type="rag",
        retrieval=True,
        memory=False,
        human_review=False,
        tool_access=["ehr_lookup"],
    )
    rec = GuardrailRecommender().recommend(profile)
    assert rec.risk_score > 0.0
    assert rec.guardrail_level.startswith("L")
    assert "audit_logger" in rec.required_controls


def test_search_smoke(tmp_path) -> None:
    benchmark = BenchmarkSpec.from_yaml("examples/benchmark.healthcare.yaml")
    search = EvoGuardSearch.from_yaml("examples/search.healthcare.yaml")
    result = search.run(benchmark)
    assert result.generations == 8
    assert len(result.best_candidates) > 0

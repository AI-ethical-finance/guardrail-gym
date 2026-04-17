from guardrail_gym.benchmark.spec import BenchmarkSpec

BENCHMARK = "examples/benchmark.regulated.yaml"

def main():
    benchmark = BenchmarkSpec.from_yaml(BENCHMARK)

    bereavement = benchmark.scenarios_for_vulnerability("bereavement")
    chronic = benchmark.scenarios_for_vulnerability("chronic_illness")
    edge = benchmark.scenarios_for_deployment("edge_device")
    enterprise = benchmark.scenarios_for_deployment("enterprise_gpu")
    healthcare = benchmark.scenarios_for_environment("healthcare_strict")
    finance = benchmark.scenarios_for_environment("finance_consumer")

    print("bereavement scenarios:", len(bereavement))
    print("chronic illness scenarios:", len(chronic))
    print("edge deployment scenarios:", len(edge))
    print("enterprise deployment scenarios:", len(enterprise))
    print("healthcare_strict scenarios:", len(healthcare))
    print("finance_consumer scenarios:", len(finance))

if __name__ == "__main__":
    main()

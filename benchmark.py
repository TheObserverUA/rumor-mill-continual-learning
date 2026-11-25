import contextlib
import io
import random
from rumor_mill_sim import MAX_PROBES, RumorMillEngine

SCENARIOS = {
    "Standard Insights": {
        "flags": {},
        "actions": ["ELABORATION", "DISRUPTION", "POLITE", "REJECTION", "DEBUNK"],
        "weights": [0.35, 0.20, 0.15, 0.15, 0.15],
    },
    "Niche / Complex (x2)": {
        "flags": {"is_niche": True},
        "actions": ["ELABORATION", "DISRUPTION", "POLITE", "REJECTION", "DEBUNK"],
        "weights": [0.42, 0.23, 0.12, 0.14, 0.09],
    },
    "Viral Hype / Fakes (3.0)": {
        "flags": {"is_hype": True},
        "actions": ["ELABORATION", "DISRUPTION", "POLITE", "REJECTION", "DEBUNK"],
        "weights": [0.42, 0.22, 0.06, 0.10, 0.20],
    },
    "Polarized Debates (50/50)": {
        "flags": {},
        "actions": ["ELABORATION", "DISRUPTION", "POLITE", "REJECTION", "DEBUNK"],
        "weights": [0.28, 0.15, 0.12, 0.42, 0.03],
    },
    "Bot-Farm Poisoning": {
        "flags": {"bot": True},
        "actions": ["ELABORATION"],
        "weights": [1.0],
    },
}


def run_batch(runs: int = 500, seed: int = 42):
    print(f"\n=== BENCHMARK RUN (N={runs} per category, seed={seed}) ===")
    header = f"{'Scenario Category':<26} | {'Promoted':>8} | {'Pruned':>8} | {'Dormant':>8} | {'Unresolved':>10}"
    print(header)
    print("-" * len(header))

    for name, cfg in SCENARIOS.items():
        rng = random.Random(seed)
        counts = {"HYPOTHESIS": 0, "PRUNED": 0, "DORMANT": 0, "RUMOR": 0}

        with contextlib.redirect_stdout(io.StringIO()):
            for i in range(runs):
                eng = RumorMillEngine()
                node = eng.add_rumor(f"{name[:3]}_{i}", f"Sample {name} #{i}", **cfg["flags"])
                for _ in range(MAX_PROBES):
                    if node.status != "RUMOR":
                        break
                    reaction = rng.choices(cfg["actions"], weights=cfg["weights"], k=1)[0]
                    eng.probe(node, reaction)
                counts[node.status] += 1

        p = counts["HYPOTHESIS"] / runs * 100
        d = counts["PRUNED"] / runs * 100
        a = counts["DORMANT"] / runs * 100
        u = counts["RUMOR"] / runs * 100
        print(f"{name:<26} | {p:7.1f}% | {d:7.1f}% | {a:7.1f}% | {u:9.1f}%")


if __name__ == "__main__":
    run_batch(runs=500, seed=42)
    run_batch(runs=500, seed=101)

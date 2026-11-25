import random
from dataclasses import dataclass
from typing import List

@dataclass
class MemoryItem:
    id: str
    content: str
    status: str = "RUMOR"
    emotional_volatility: float = 0.0
    bot_spike_flag: bool = False
    synaptic_weight: float = 0.0
    probe_count: int = 0
SYNAPTIC_WEIGHTS = {
    "COGNITIVE_DISRUPTION": 0.6,
    "CONSTRUCTIVE_ELABORATION": 0.8,
    "POLITE_COMPLIANCE": 0.1,
    "VISCERAL_REJECTION": -0.6,
    "FACTUAL_DEBUNKING": -1.5,
}

class RumorMillEngine:
    def __init__(self):
        self.quarantine_buffer: List[MemoryItem] = []
        self.consolidated_knowledge: List[MemoryItem] = []
        self.dormant_archive: List[MemoryItem] = []
      def thalamus_gate(self, query: str, is_bot_pattern: bool = False) -> bool:
        if is_bot_pattern:
            print(f"[THALAMUS GATE] Blocked bot pattern: '{query}'")
            return False
        routine = ["weather", "time", "translate", "hello"]
        is_novel = not any(w in query.lower() for w in routine)
        print(f"[THALAMUS GATE] '{query}' -> Passed: {is_novel}")
        return is_novel
    def sleep_consolidation(self, session_id: str, insight: str, volatility: float = 0.1, bot_spike: bool = False):
        item = MemoryItem(id=session_id, content=insight, emotional_volatility=volatility, bot_spike_flag=bot_spike)
        self.quarantine_buffer.append(item)
        print(f"[HIPPOCAMPUS SLEEP] Archived '{item.content}' -> Status: {item.status}")
    def adversarial_cross_probe(self, item: MemoryItem, reaction_type: str):
        if item.bot_spike_flag:
            item.status = "PRUNED"
            self.quarantine_buffer.remove(item)
            print(f"[INNATE IMMUNITY] Bot spike pruned: '{item.content}'")
            return
        delta = SYNAPTIC_WEIGHTS.get(reaction_type, 0.0)
        item.synaptic_weight = round(item.synaptic_weight + delta, 2)
        item.probe_count += 1
        print(f"[PROBE #{item.probe_count}] {reaction_type} ({delta:+}) -> Net Weight: {item.synaptic_weight}")
        if reaction_type == "FACTUAL_DEBUNKING" and item.synaptic_weight <= -1.0:
            item.status = "PRUNED"
            self.quarantine_buffer.remove(item)
            print("[MICROGLIA PRUNING] Factually debunked. Deleted.")
        elif item.synaptic_weight >= 1.0:
            item.status = "HYPOTHESIS"
            self.quarantine_buffer.remove(item)
            self.consolidated_knowledge.append(item)
            print("[ACTION POTENTIAL] Threshold reached! Promoted to HYPOTHESIS.")
        elif item.synaptic_weight <= -1.0:
            item.status = "DORMANT"
            self.quarantine_buffer.remove(item)
            self.dormant_archive.append(item)
            print("[GALILEO ARCHIVE] Visceral skepticism without proof. Moved to 3-year DORMANT state.")
        elif item.probe_count >= 4 and -0.3 <= item.synaptic_weight <= 0.3:
            print("[DEADLOCK 50/50] Polarized tie. Convening Stochastic Human Jury...")
            self.stochastic_human_jury(item)
    def stochastic_human_jury(self, item: MemoryItem):
        votes = [random.choice(["APPROVE", "REJECT"]) for _ in range(5)]
        approvals = votes.count("APPROVE")
        print(f"[STOCHASTIC JURY] Votes: {votes} ({approvals}/5 approved)")
        if approvals >= 3:
            item.status = "HYPOTHESIS"
            self.consolidated_knowledge.append(item)
            print("[JURY VERDICT] Promoted to HYPOTHESIS.")
        else:
            item.status = "PRUNED"
            print("[JURY VERDICT] Pruned from memory.")
        if item in self.quarantine_buffer:
            self.quarantine_buffer.remove(item)
if __name__ == "__main__":
    print("=== INITIALIZING RUMOR MILL CONTINUAL LEARNING SIMULATION ===\n")
    engine = RumorMillEngine()

    engine.thalamus_gate("What is the weather in Kyiv today?")
    engine.thalamus_gate("Buy crypto token X1000 now", is_bot_pattern=True)
    print("-" * 60)

    engine.sleep_consolidation("SESS_BOT_99", "Token X1000 gives 1000% profit", bot_spike=True)
    engine.adversarial_cross_probe(engine.quarantine_buffer[0], "CONSTRUCTIVE_ELABORATION")
    print("-" * 60)
    engine.sleep_consolidation("SESS_USER_01", "Use sleep-time pruning instead of weight mutation")
    item1 = engine.quarantine_buffer[0]
    engine.adversarial_cross_probe(item1, "VISCERAL_REJECTION")
    engine.adversarial_cross_probe(item1, "COGNITIVE_DISRUPTION")
    engine.adversarial_cross_probe(item1, "POLITE_COMPLIANCE")
    engine.adversarial_cross_probe(item1, "CONSTRUCTIVE_ELABORATION")
    print("-" * 60)

    engine.sleep_consolidation("SESS_GALILEO_02", "Quantum entanglement routes agent memory")
    item2 = engine.quarantine_buffer[0]
    engine.adversarial_cross_probe(item2, "VISCERAL_REJECTION")
    engine.adversarial_cross_probe(item2, "VISCERAL_REJECTION")
    print("-" * 60)

    print("\n=== FINAL CONSOLIDATED KNOWLEDGE BASE ===")
    for k in engine.consolidated_knowledge:
        print(f" - [{k.status}] {k.content}")
    print("\n=== DORMANT ('GALILEO') ARCHIVE ===")
    for d in engine.dormant_archive:
        print(f" - [{d.status}] {d.content}")


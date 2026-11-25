import time
import random
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MemoryItem:
    id: str
    content: str
    status: str = "RUMOR"  # RUMOR -> HYPOTHESIS -> PRUNED
    emotional_volatility: float = 0.0
    bot_spike_flag: bool = False
    engagement_score: float = 0.0

class RumorMillEngine:
    def __init__(self):
        self.quarantine_buffer: List[MemoryItem] = []
        self.consolidated_knowledge: List[MemoryItem] = []

    def thalamus_gate(self, query: str) -> bool:
        """Filters out routine queries to save compute (Thalamic Gating)."""
        routine_keywords = ["weather", "time", "translate", "hello"]
        is_novel = not any(word in query.lower() for word in routine_keywords) and len(query.split()) > 4
        print(f"[THALAMUS GATE] Query: '{query}' -> Novelty Passed: {is_novel}")
        return is_novel

    def sleep_consolidation(self, session_id: str, extracted_insight: str, volatility: float = 0.1, bot_spike: bool = False):
        """Extracts anonymized insights into quarantine after session closes."""
        item = MemoryItem(
            id=session_id,
            content=extracted_insight,
            emotional_volatility=volatility,
            bot_spike_flag=bot_spike
        )
        self.quarantine_buffer.append(item)
        print(f"[HIPPOCAMPUS SLEEP] Archived '{item.content}' -> Status: {item.status} (BotFlag={bot_spike}, Volatility={volatility})")

    def adversarial_cross_probe(self, item: MemoryItem, orthogonal_user_reaction: str):
        """Tests unverified rumors on orthogonal/skeptical user profiles via follow-ups."""
        print(f"\n[ADVERSARIAL PROBE] Injecting '{item.content}' as optional follow-up to orthogonal skeptic...")
        
        if item.emotional_volatility > 0.7:
            print(f"[COOLDOWN MODULE] High emotional volatility ({item.emotional_volatility}). Enforcing Temporal Timeout before probing.")

        if orthogonal_user_reaction == "DEBUNKED":
            item.status = "PRUNED"
            self.quarantine_buffer.remove(item)
            print(f"[MICROGLIA PRUNING] Skeptic debunked rumor. Memory deleted.")
        elif orthogonal_user_reaction == "RESONANCE":
            item.status = "HYPOTHESIS"
            self.quarantine_buffer.remove(item)
            self.consolidated_knowledge.append(item)
            print(f"[CONSOLIDATED] Intellectual resonance achieved! Promoted to {item.status}.")
        elif orthogonal_user_reaction == "TIE_50_50":
            print(f"[DEADLOCK 50/50] Deterministic logic halted. Convening Stochastic Human Jury...")
            self.stochastic_human_jury(item)

    def stochastic_human_jury(self, item: MemoryItem):
        """Resolves 50/50 ambiguity via anonymized cross-cultural human cohort."""
        jury_votes = [random.choice(["APPROVE", "REJECT"]) for _ in range(5)]
        approvals = jury_votes.count("APPROVE")
        print(f"[STOCHASTIC JURY] Cohort votes: {jury_votes} ({approvals}/5 approved)")
        
        if approvals >= 3:
            item.status = "HYPOTHESIS"
            self.consolidated_knowledge.append(item)
            print(f"[JURY VERDICT] Promoted to {item.status}.")
        else:
            item.status = "PRUNED"
            print(f"[JURY VERDICT] Pruned from memory.")
        if item in self.quarantine_buffer:
            self.quarantine_buffer.remove(item)

if __name__ == "__main__":
    print("=== INITIALIZING RUMOR MILL CONTINUAL LEARNING SIMULATION ===\n")
    engine = RumorMillEngine()

    # 1. Routine query filtered by Thalamus
    engine.thalamus_gate("What is the weather in Kyiv today?")
    print("-" * 60)

    # 2. Bot farm attack simulation
    if engine.thalamus_gate("Buy miracle crypto token X1000 guaranteed profit now"):
        engine.sleep_consolidation("SESS_BOT_99", "Crypto token X1000 guarantees 1000% return", volatility=0.2, bot_spike=True)
        engine.adversarial_cross_probe(engine.quarantine_buffer[0], orthogonal_user_reaction="DEBUNKED")
    print("-" * 60)

    # 3. Genuine novel insight simulation
    if engine.thalamus_gate("Can microglial pruning algorithms prevent LLM catastrophic forgetting?"):
        engine.sleep_consolidation("SESS_USER_01", "Use sleep-time pruning instead of weight mutation", volatility=0.1)
        engine.adversarial_cross_probe(engine.quarantine_buffer[0], orthogonal_user_reaction="RESONANCE")
    print("-" * 60)

    # 4. High-volatility 50/50 ethical dilemma simulation
    if engine.thalamus_gate("Should autonomous agents prioritize speed over transparency in emergencies?"):
        engine.sleep_consolidation("SESS_DILEMMA_07", "Bypass transparency logs during critical crisis", volatility=0.85)
        engine.adversarial_cross_probe(engine.quarantine_buffer[0], orthogonal_user_reaction="TIE_50_50")

    print("\n=== FINAL CONSOLIDATED KNOWLEDGE BASE ===")
    for k in engine.consolidated_knowledge:
        print(f" - [{k.status}] {k.content}")

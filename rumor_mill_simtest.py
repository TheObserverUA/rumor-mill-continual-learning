import random
from dataclasses import dataclass, field
from typing import List, Optional

WEIGHTS = {"DISRUPTION": 0.6, "ELABORATION": 0.8, "POLITE": 0.1, "REJECTION": -0.6, "DEBUNK": -1.5}
MAX_PROBES = 6
@dataclass
class MemoryNode:
    id: str
    content: str
    parent: Optional["MemoryNode"] = None
    status: str = "RUMOR"
    weight: float = 0.0
    probes: int = 0
    is_niche: bool = False
    is_hype: bool = False
    bot_flag: bool = False
    children: List["MemoryNode"] = field(default_factory=list)
class RumorMillEngine:
    def __init__(self):
        self.quarantine, self.knowledge, self.dormant = [], [], []

    def _detach(self, node: MemoryNode):
        if node in self.quarantine:
            self.quarantine.remove(node)
        if node in self.knowledge:
            self.knowledge.remove(node)
        if node.parent and node in node.parent.children:
            node.parent.children.remove(node)

    def add_rumor(self, node_id: str, text: str, parent: Optional[MemoryNode] = None, is_niche=False, is_hype=False, bot=False) -> MemoryNode:
        node = MemoryNode(node_id, text, parent=parent, is_niche=is_niche, is_hype=is_hype, bot_flag=bot)
        if parent:
            parent.children.append(node)
        self.quarantine.append(node)
        print(f"[QUARANTINE] Added '{text}' (Parent: {parent.id if parent else 'None'})")
        return node
    def thalamus_gate(self, query: str, is_bot: bool = False) -> bool:
        if is_bot:
            print(f"[THALAMUS] Blocked bot pattern: '{query}'")
            return False
        routine = ("weather", "time", "translate", "hello")
        passed = not any(w in query.lower() for w in routine)
        print(f"[THALAMUS] '{query}' -> Passed: {passed}")
        return passed

    def probe(self, node: MemoryNode, reaction: str):
        if node.status in ("PRUNED", "DORMANT"):
            return

        if node.bot_flag:
            node.status = "PRUNED"
            self._detach(node)
            print(f"[IMMUNITY] Bot pruned: '{node.content}'")
            return

        if node.status == "HYPOTHESIS":
            if reaction == "DEBUNK":
                node.status = "PRUNED"
                self._detach(node)
                print(f"[LTP OVERRIDE] Debunked hypothesis: '{node.content}'")
            else:
                print(f"[LTP SHIELD] Noise '{reaction}' ignored for verified hypothesis.")
            return
        if reaction == "DEBUNK":
            node.status = "PRUNED"
            self._detach(node)
            print(f"[PRUNED] Factually debunked '{node.id}'. Parent '{node.parent.id if node.parent else 'None'}' safe!")
            return

        delta = WEIGHTS.get(reaction, 0.0)
        if node.is_niche and delta > 0:
            delta *= 2.0

        node.weight = round(node.weight + delta, 2)
        node.probes += 1
        threshold = 3.0 if node.is_hype else 1.0
        print(f"[PROBE #{node.probes}] '{node.content[:25]}...' | {reaction} ({delta:+}) -> Net: {node.weight}/{threshold}")

        if node.weight >= threshold:
            node.status = "HYPOTHESIS"
            self.quarantine.remove(node)
            self.knowledge.append(node)
            print(f"[PROMOTED] '{node.content}' -> HYPOTHESIS!")
        elif node.weight <= -1.0:
            node.status = "DORMANT"
            self._detach(node)
            self.dormant.append(node)
            print(f"[GALILEO] '{node.content}' -> 3-year DORMANT.")
        elif node.probes >= MAX_PROBES or (node.probes >= 4 and -0.4 <= node.weight <= 0.4):
            votes = [random.choice(["APPROVE", "REJECT"]) for _ in range(5)]
            ok = votes.count("APPROVE") >= 3
            node.status = "HYPOTHESIS" if ok else "PRUNED"
            self._detach(node)
            if ok:
                self.knowledge.append(node)
            print(f"[STOCHASTIC JURY] {votes} -> Verdict: {node.status}")
if __name__ == "__main__":
    print("=== RUMOR MILL CONTINUAL LEARNING ENGINE v1.0 ===\n")
    eng = RumorMillEngine()

    eng.thalamus_gate("What is the weather in Kyiv?")
    eng.thalamus_gate("Buy crypto token X1000 now", is_bot=True)
    print("-" * 55)

    root = eng.add_rumor("V1", "Base insight: freeze LLM weights")
    branch = eng.add_rumor("V2", "Bad verse: mutate weights on Sundays", parent=root)
    eng.probe(branch, "ELABORATION")
    eng.probe(branch, "DEBUNK")

    eng.probe(root, "ELABORATION")
    eng.probe(root, "DISRUPTION")
    eng.probe(root, "REJECTION")
    print("-" * 55)

    niche = eng.add_rumor("N1", "Rare kernel race-condition fix", is_niche=True)
    eng.probe(niche, "ELABORATION")

    hype = eng.add_rumor("H1", "Viral conspiracy rumor", is_hype=True)
    eng.probe(hype, "ELABORATION")
    eng.probe(hype, "ELABORATION")

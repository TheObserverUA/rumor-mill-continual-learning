import random
from dataclasses import dataclass, field
from typing import List, Optional

WEIGHTS = {"DISRUPTION": 0.6, "ELABORATION": 0.8, "POLITE": 0.1, "REJECTION": -0.6, "DEBUNK": -1.5}

@dataclass
class MemoryNode:
    id: str
    content: str
    parent: Optional['MemoryNode'] = None
    status: str = "RUMOR"
    weight: float = 0.0
    probes: int = 0
    is_niche: bool = False
    is_hype: bool = False
    bot_flag: bool = False
    children: List['MemoryNode'] = field(default_factory=list)
class RumorMillEngine:
    def __init__(self):
        self.quarantine, self.knowledge, self.dormant = [], [], []

    def add_rumor(self, node_id: str, text: str, parent: Optional[MemoryNode] = None, is_niche=False, is_hype=False, bot=False) -> MemoryNode:
        node = MemoryNode(node_id, text, parent=parent, is_niche=is_niche, is_hype=is_hype, bot_flag=bot)
        if parent:
            parent.children.append(node)
        self.quarantine.append(node)
        print(f"[QUARANTINE] Added '{text}' (Parent: {parent.id if parent else 'None'})")
        return node

    def probe(self, node: MemoryNode, reaction: str):
        if node.bot_flag:
            node.status = "PRUNED"
            self.quarantine.remove(node)
            print(f"[IMMUNITY] Bot pruned: '{node.content}'")
            return

        if node.status == "HYPOTHESIS":
            if reaction == "DEBUNK":
                node.status = "PRUNED"
                self.knowledge.remove(node)
                print(f"[LTP OVERRIDE] Factually debunked hypothesis: '{node.content}'")
            else:
                print(f"[LTP SHIELD] Emotional noise '{reaction}' ignored for verified hypothesis.")
            return

        delta = WEIGHTS.get(reaction, 0.0)
        if node.is_niche and delta > 0:
            delta *= 2.0
        node.weight = round(node.weight + delta, 2)
        node.probes += 1
        threshold = 3.0 if node.is_hype else 1.0
        print(f"[PROBE #{node.probes}] '{node.content[:25]}...' | {reaction} ({delta:+}) -> Net: {node.weight}/{threshold}")

        if reaction == "DEBUNK" and node.weight <= -1.0:
            node.status = "PRUNED"
            self.quarantine.remove(node)
            print(f"[PRUNED] Branch '{node.id}' deleted. Parent '{node.parent.id if node.parent else 'None'}' safe!")
        elif node.weight >= threshold:
            node.status = "HYPOTHESIS"
            self.quarantine.remove(node)
            self.knowledge.append(node)
            print(f"[PROMOTED] '{node.content}' -> HYPOTHESIS!")
        elif node.weight <= -1.0:
            node.status = "DORMANT"
            self.quarantine.remove(node)
            self.dormant.append(node)
            print(f"[GALILEO] '{node.content}' -> 3-year DORMANT.")

if __name__ == "__main__":
    eng = RumorMillEngine()
    root = eng.add_rumor("V1", "Base insight: freeze LLM weights")
    branch = eng.add_rumor("V2", "Bad verse: mutate weights on Sundays", parent=root)
    eng.probe(branch, "DEBUNK")
    eng.probe(root, "ELABORATION")
    eng.probe(root, "DISRUPTION")
    eng.probe(root, "REJECTION")

    niche = eng.add_rumor("N1", "Rare kernel race-condition fix", is_niche=True)
    eng.probe(niche, "ELABORATION")

    hype = eng.add_rumor("H1", "Viral conspiracy rumor", is_hype=True)
    eng.probe(hype, "ELABORATION")
    eng.probe(hype, "ELABORATION")

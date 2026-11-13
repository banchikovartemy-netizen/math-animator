"""A reviewed solution contract, not a natural-language solver."""
from dataclasses import dataclass, field
from typing import Protocol
from math_engine.checks import Check

@dataclass
class Step:
    explanation: str
    formulas: list[str]
    visual: str
    transition: str

@dataclass
class Solution:
    problem: str
    goal: str
    method: str
    domain: str
    steps: list[Step]
    checks: list[Check] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

class SolutionProvider(Protocol):
    """Optional LLM adapters must return reviewable artifacts; no API is required."""
    def prepare(self, problem: str) -> Solution: ...

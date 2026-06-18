from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class WorkflowMetrics:
    llm_invoked: bool
    retrieval_hits: int
    routing_decision: str
    workflow_duration_ms: float
    extra: dict = field(default_factory=dict)


class Timer:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, *args):
        self.end = perf_counter()
        self.duration_ms = (self.end - self.start) * 1000
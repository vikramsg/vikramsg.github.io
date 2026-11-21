from dataclasses import dataclass
import re
import threading

from gepa.adapters.default_adapter.default_adapter import (
    ContainsAnswerEvaluator,
    DefaultDataInst,
    EvaluationResult,
)


@dataclass
class EvalRecord:
    input_text: str
    expected: str
    predicted: str
    raw_response: str
    score: float
    feedback: str


def extract_answer_tag(response: str) -> str:
    match = re.search(r"###\s*([^\n]+)", response)
    if match:
        return f"### {match.group(1).strip()}"
    first_line = response.strip().splitlines()[0] if response.strip() else ""
    return first_line[:40]


class RecordingEvaluator:
    """Wraps GEPA's ContainsAnswerEvaluator and records each eval for clean rendering."""

    def __init__(self) -> None:
        self._base = ContainsAnswerEvaluator()
        self._lock = threading.Lock()
        self._records: list[EvalRecord] = []

    def __call__(self, data: DefaultDataInst, response: str) -> EvaluationResult:
        res = self._base(data, response)
        record = EvalRecord(
            input_text=data["input"],
            expected=data["answer"],
            predicted=extract_answer_tag(response),
            raw_response=response.strip(),
            score=res.score,
            feedback=res.feedback,
        )
        with self._lock:
            self._records.append(record)
        return res

    def drain(self) -> list[EvalRecord]:
        with self._lock:
            items = list(self._records)
            self._records.clear()
        return items

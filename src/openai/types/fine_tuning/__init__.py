from typing import TypedDict, Optional, List


class FineTuningJob(TypedDict, total=False):
    id: str
    status: str
    model: str
    hyperparameters: dict
    integrations: Optional[List[dict]]


__all__ = ["FineTuningJob"]

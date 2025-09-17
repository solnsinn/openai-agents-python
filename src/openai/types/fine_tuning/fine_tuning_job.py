from typing import Optional, List, Dict, Any
from typing_extensions import TypedDict


class Hyperparameters(TypedDict, total=False):
    # Minimal placeholder for hyperparameter mapping used by litellm
    learning_rate: Optional[float]
    batch_size: Optional[int]
    epochs: Optional[int]


class FineTuningJob(TypedDict, total=False):
    id: str
    object: str
    status: str
    model: str
    hyperparameters: Optional[Hyperparameters]
    integrations: Optional[List[Dict[str, Any]]]


__all__ = ["FineTuningJob", "Hyperparameters"]

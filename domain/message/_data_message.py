from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass
class Message(Generic[T]):
    content: T
    timestamp: float

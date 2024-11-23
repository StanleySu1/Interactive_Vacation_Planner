from pydantic import BaseModel, Json
from pydantic_core import from_json
from typing import Any, Callable, Optional
from collections.abc import Sequence, MutableSequence

class Review(BaseModel):
  review: str = ""
  rating: float = 5.0
  visited: str = ""

class Attraction(BaseModel):
  name: str = ""
  category: str = ""
  hours: str = ""
  address: str = ""
  rating: int = 0
  reviews: MutableSequence[Review] = []
  # data: Optional[Json[Any]] = None

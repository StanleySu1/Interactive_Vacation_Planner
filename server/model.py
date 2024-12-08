from pydantic import BaseModel, Json
from pydantic_core import from_json
from typing import Any, Callable, Optional
from collections.abc import Sequence, MutableSequence

class Review(BaseModel):
  title: str = ""
  review: str = ""
  rating: float = 5.0
  visited: str = ""

class Attraction(BaseModel):
  name: str = ""
  description: str = ""
  category: str = ""
  breadcrumbs: MutableSequence[str] = []
  hours: str = ""
  duration: str = ""
  address: str = ""
  neighborhood: str = ""
  rating: int = 0
  getting_there: MutableSequence[str] = []
  top_reviews: MutableSequence[Review] = []
  reviews: MutableSequence[Review] = []
  images: MutableSequence[str] = []
  # data: Optional[Json[Any]] = None

from pydantic import BaseModel
from typing import List, Tuple



class VectorData(BaseModel):
    id: str
    vector: List[float]

class SearchQuery(BaseModel):
    vector: List[float]
    k: int = 5

class SearchResult(BaseModel):
    id: str
    score: float
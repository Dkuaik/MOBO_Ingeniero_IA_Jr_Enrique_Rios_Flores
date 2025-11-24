from pydantic import BaseModel
from typing import List, Tuple, Dict, Any



class VectorData(BaseModel):
    id: str
    vector: List[float]
    metadata: Dict[str, Any] = {}

class SearchQuery(BaseModel):
    vector: List[float]
    k: int = 5
    role_id: int = 4

class SearchResult(BaseModel):
    id: str
    score: float
    metadata: Dict[str, Any] = {}
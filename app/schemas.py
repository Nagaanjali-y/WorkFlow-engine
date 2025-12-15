from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Condition(BaseModel):
    key: str
    operator: str
    value: Any
    target_if_true: str
    target_if_false: str

class Edge(BaseModel):
    from_node: str
    to_node: Optional[str] = None
    condition: Optional[Condition] = None

class GraphCreateRequest(BaseModel):
    name: str
    nodes: List[str]
    edges: List[Edge]
    start_node: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
from typing import List, Dict, Any, Literal
from typing_extensions import TypedDict

class GraphState(TypedDict):
    input_mode: Literal["manual", "auto"]
    raw_input: str  # The user prompt or uploaded script text
    script: Dict[str, Any]  # Will hold the scene segments
    characters: List[Dict[str, Any]]
    images: List[str] # Paths to generated images
    status: str
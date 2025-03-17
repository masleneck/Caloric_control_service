from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TestQuestionResponse(BaseModel):
    id: int
    text: str
    type: str
    options: Optional[List[str]]
    
    model_config = ConfigDict(from_attributes=True)
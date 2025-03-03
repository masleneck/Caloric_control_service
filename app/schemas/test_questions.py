from pydantic import BaseModel
from typing import List, Optional

class TestQuestionResponse(BaseModel):
    '''Схема ответа с вопросами'''
    id: int
    text: str
    type: str
    options: Optional[List[str]] = None

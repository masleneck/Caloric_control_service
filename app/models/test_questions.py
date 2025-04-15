import enum
from sqlalchemy import JSON, String, text as txt
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class QuestionType(enum.Enum):
    """Тип вопроса"""
    options = "options"
    input = "input"
    NOT_STATED = "NOT_STATED"

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    __tablename__ = "test_questions"

    name: Mapped[str] = mapped_column(
        String(100),
    )
    text: Mapped[str] = mapped_column(
        String(255),
    )
    type: Mapped[QuestionType] = mapped_column(
        default = QuestionType.NOT_STATED, 
        server_default = txt("'NOT_STATED'"),
    )
    options: Mapped[list[str] | None] = mapped_column(
        JSON,
    )
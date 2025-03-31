from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base

class Mealtime(enum.Enum):
    """Тип приема пищи"""
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"

class Meals(Base):
    """Хранит приемы пищи"""
    __tablename__ = "meals"

    mealtime: Mapped[Mealtime] = mapped_column(default = Mealtime.SNACK, server_default = text("'SNACK'"))
    meal_date: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        back_populates="meals",
        lazy="joined",
    )

    # Связь многие-ко-многим с FoodItem через MealFoodItem
    food_items: Mapped[list["FoodItems"]]= relationship(
        back_populates="meals",
        secondary="meal_food_items", # название таблицы, через которую связы 
        lazy="selectin",
    )

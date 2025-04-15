from datetime import date
from sqlalchemy import ForeignKey, Date, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

class Mealtime(enum.Enum):
    """Тип приема пищи"""
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"

class Meal(Base):
    """Хранит приемы пищи"""
    __tablename__ = "meals"

    mealtime: Mapped[Mealtime] = mapped_column(
        default = Mealtime.SNACK,
        server_default = text("'SNACK'"),
    )
    meal_date: Mapped[date] = mapped_column(
        Date,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    
    # Связь многие-к-одному с User
    user: Mapped["User"] = relationship(
        back_populates="meals",
        lazy="joined",
    )

    # Связь многие-ко-многим с FoodItem через MealFoodItem
    food_items: Mapped[list["FoodItem"]]= relationship(
        back_populates="meals",
        secondary="meal_food_items", # название таблицы, через которую связы 
        lazy="selectin",
        viewonly=True,
    )

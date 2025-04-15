from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class FoodItem(Base):
    """Хранит продукты"""
    __tablename__ = "food_items"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )
    calories: Mapped[float] = mapped_column(
        Float,
    )
    proteins: Mapped[float] = mapped_column(
        Float,
    )
    fats: Mapped[float] = mapped_column(
        Float,
    )
    carbs: Mapped[float] = mapped_column(
        Float,
    )

    # Связь многие-ко-многим с Meal через MealFoodItem
    meals: Mapped[list["Meal"]]= relationship(
        back_populates="food_items",
        secondary="meal_food_items", # название таблицы, через которую связы
        lazy="selectin",
        viewonly=True,
    )
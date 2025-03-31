from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class FoodItems(Base):
    """Хранит продукты"""
    __tablename__ = "food_items"

    name: Mapped[str] = mapped_column(unique=True)
    calories: Mapped[float]
    proteins: Mapped[float] 
    fats: Mapped[float] 
    carbs: Mapped[float] 

    # Связь многие-ко-многим с Meal через MealFoodItem
    meals: Mapped[list["Meals"]]= relationship(
        back_populates="food_items",
        secondary="meal_food_items", # название таблицы, через которую связы
        lazy="selectin",
    )
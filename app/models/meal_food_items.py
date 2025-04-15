from sqlalchemy import Float, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class MealFoodItem(Base):
    """Связь приемов пищи и продуктов"""
    __tablename__ = "meal_food_items"
    __table_args__ = (
        Index("idx_meal_food_meal_id", "meal_id"),  # Для поиска по meal_id
        Index("idx_meal_food_food_id", "food_item_id"),  # Для поиска по food_item_id
        Index("idx_meal_food_composite", "meal_id", "food_item_id", unique=True),  # Композитный индекс
    )

    meal_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("meals.id", ondelete="CASCADE"),
        primary_key=True,
    )
    food_item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("food_items.id", ondelete="CASCADE"),
        primary_key=True,
    )
    quantity: Mapped[float] = mapped_column(
        Float,
    )


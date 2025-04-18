from sqlalchemy import Float, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class FoodItem(Base):
    """Хранит продукты"""
    __tablename__ = "food_items"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
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
    __table_args__ = (
        # Триграммный индекс для func.similarity() и нечеткого поиска
        Index(
            'ix_food_items_name_trgm', 
            name, 
            postgresql_using='gin',
            postgresql_ops={'name': 'gin_trgm_ops'}
        ),
        # Индекс для точного совпадения (регистронезависимого)
        Index(
            'ix_food_items_name_lower',
            func.lower(name),
            postgresql_using='btree'
        ),
        # Индекс для ILIKE поиска (опционально, если часто используете)
        Index(
            'ix_food_items_name_ilike',
            name,
            postgresql_using='gin',
            postgresql_ops={'name': 'gin_trgm_ops'}  # Тот же триграммный индекс работает и для ILIKE
        ),
    )
    
    # Связь многие-ко-многим с Meal через MealFoodItem
    meals: Mapped[list["Meal"]]= relationship(
        back_populates="food_items",
        secondary="meal_food_items", # название таблицы, через которую связы
        lazy="selectin",
        viewonly=True,
    )
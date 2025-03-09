from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db import Base

class FoodItem(Base):
    '''Хранит продукты'''
    __tablename__ = 'food_items'

    name: Mapped[str] = mapped_column(unique=True)
    calories: Mapped[float]
    proteins: Mapped[float] 
    fats: Mapped[float] 
    carbs: Mapped[float] 

     # Связь многие-ко-многим с Meal через MealFoodItem
    meals: Mapped[list['Meal']] = relationship(
        'Meal',
        secondary='meal_food_items',
        back_populates='food_items'
    )

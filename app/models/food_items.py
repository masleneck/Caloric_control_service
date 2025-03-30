# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.core.database import Base

# class FoodItem(Base):
#     '''Хранит продукты'''
#     __tablename__ = 'food_items'

#     name: Mapped[str] = mapped_column(unique=True)
#     calories: Mapped[float]
#     proteins: Mapped[float] 
#     fats: Mapped[float] 
#     carbs: Mapped[float] 

#     # Связь многие-ко-многим с Meal через MealFoodItem
#     meals: Mapped[list['Meal']] = relationship(
#         'Meal',
#         secondary='meal_food_items',
#         back_populates='food_items',
#         overlaps='meal_food_links, meal'
#     )

#     meal_food_links: Mapped[list['MealFoodItem']] = relationship(
#     'MealFoodItem',
#     back_populates='food_item',
#     overlaps='meals, food_items'
#     )
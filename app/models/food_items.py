from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

class FoodItem(Base):
    '''Хранит продукты'''
    __tablename__ = 'food_items'

    name: Mapped[str] = mapped_column(unique=True)
    calories: Mapped[float]
    proteins: Mapped[float] 
    fats: Mapped[float] 
    carbs: Mapped[float] 


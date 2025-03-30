import asyncio
from faker import Faker
from loguru import logger
from app.core.database import Base, async_session_maker, check_db_connection, async_engine
from app.models import User, Profile, TestResult
from app.utils.auth_utils import get_password_hash

fake = Faker('ru_RU')

async def create_test_users(count: int = 50):
    """Создает тестовых пользователей с профилями"""
    async with async_session_maker() as session:
        for i in range(1, count + 1):
            # Создаем пользователя
            user = User(
                email=f"testuser{i}@example.com",
                password=get_password_hash("TestPassword123!"),
                is_superuser=False
            )
            session.add(user)
            await session.flush()  # Получаем ID
            
            # Создаем профиль
            profile = Profile(
                user_id=user.id,
                name=fake.first_name(),
                last_name=fake.last_name(),
                gender=fake.random_element(('MALE', 'FEMALE')),
                weight=fake.random_int(50, 120),
                height=fake.random_int(150, 200),
                goal=fake.random_element(('LOSE_WEIGHT', 'KEEPING_FIT', 'GAIN_MUSCLE_MASS')),
                birthday_date=fake.date_of_birth(minimum_age=18, maximum_age=70),
                activity_level=fake.random_element(('SEDENTARY', 'LIGHT', 'MODERATE','ACTIVE','ATHLETE'))
            )
            session.add(profile)
            
            # Создаем тестовый результат (опционально)
            test_result = TestResult(
                user_id=user.id,
                gender=profile.gender,
                weight=profile.weight,
                height=profile.height,
                goal=profile.goal,
                birthday_date=profile.birthday_date
            )
            session.add(test_result)
            
            if i % 10 == 0:  # Периодически коммитим
                await session.commit()
                logger.info(f"Created {i} users")
        
        await session.commit()  # Фиксируем оставшихся
        logger.success(f"Successfully created {count} test users")

async def reset_db():
    """Сброс и инициализация БД с тестовыми данными"""
    if not await check_db_connection():
        raise RuntimeError("Database connection failed")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Tables dropped")
        await conn.run_sync(Base.metadata.create_all)
        logger.success("Tables created")
    
    # Создаем тестовых пользователей
    await create_test_users(50)

if __name__ == "__main__":
    asyncio.run(reset_db())
    
    # py -m tests.test_db
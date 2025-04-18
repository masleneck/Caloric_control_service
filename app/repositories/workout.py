from datetime import date
from typing import List
from sqlalchemy import and_, func, or_, select, delete
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from loguru import logger
from app.models import Workout, UserWorkout
from app.repositories.base import BaseDAO
from app.schemas.workouts import DailyWorkoutsResponse, DailyWorkoutsSummaryResponse, WorkoutItemResponse, WorkoutUpsertRequest, WorkoutSearchItemResponse

class WorkoutDAO(BaseDAO[Workout]):
    model = Workout

    async def upsert_workouts(
        self,
        user_id: int,
        workout_data: WorkoutUpsertRequest,
    ) -> list[dict]:
        """Метод для создания/обновления тренировок пользователя"""
        # Проверяем соответствие длин списков
        if (len(workout_data.workout_names) != len(workout_data.workouts_duration_minutes) or
            len(workout_data.workout_names) != len(workout_data.workouts_calories_burned)):
            raise HTTPException(400,detail="Количество тренировок, продолжительности и калорий должно совпадать")

        # Проверяем существование тренировок в базе
        capitalized_names = [name.capitalize() for name in workout_data.workout_names]
        stmt = select(Workout).where(Workout.name.in_(capitalized_names))
        result = await self._session.execute(stmt)
        db_workouts = result.scalars().all()

        if len(db_workouts) != len(capitalized_names):
            found_names = {workout.name for workout in db_workouts}
            not_found = [name for name in capitalized_names if name not in found_names]
            raise HTTPException(404,detail=f"Тренировки не найдены: {', '.join(not_found)}")

        # Получаем существующие тренировки пользователя на эту дату
        stmt = select(UserWorkout).where(
            UserWorkout.user_id == user_id,
            UserWorkout.workout_date == workout_data.workout_date,
            UserWorkout.workout_id.in_([w.id for w in db_workouts])
        )
        result = await self._session.execute(stmt)
        existing_workouts = result.scalars().all()
        existing_mapping = {uw.workout_id: uw for uw in existing_workouts}

        workout_mapping = {w.name: w for w in db_workouts}
        result_workouts = []

        for i, workout_name in enumerate(capitalized_names):
            workout = workout_mapping[workout_name]
            
            if workout.id in existing_mapping:
                # Обновляем существующую запись
                existing = existing_mapping[workout.id]
                existing.duration_minutes = workout_data.workouts_duration_minutes[i]
                existing.calories_burned = workout_data.workouts_calories_burned[i]
                result_workouts.append(existing)
            else:
                # Создаем новую запись
                new_workout = UserWorkout(
                    user_id=user_id,
                    workout_id=workout.id,
                    workout_date=workout_data.workout_date,
                    duration_minutes=workout_data.workouts_duration_minutes[i],
                    calories_burned=workout_data.workouts_calories_burned[i]
                )
                self._session.add(new_workout)
                result_workouts.append(new_workout)

        await self._session.commit()
        
        # Формируем результат
        workout_items = [
            {
                "name": name,
                "duration": dur,
                "calories": cal
            }
            for name, dur, cal in zip(
                workout_data.workout_names,
                workout_data.workouts_duration_minutes,
                workout_data.workouts_calories_burned
            )
        ]
        
        return {
            "workout_date": workout_data.workout_date,
            "workout_items": workout_items
        }
    


    async def search_workouts(
        self,
        query: str,
        limit: int = 10,
        threshold: float = 0.3
    ) -> List[WorkoutSearchItemResponse]:
        """
        поиск тренировок с комбинацией методов:
        - Сначала точное совпадение (регистронезависимое)
        - Затем триграммный поиск (pg_trgm) для нечеткого соответствия
        - В конце простой LIKE для остальных случаев
        -- !!! Включите расширение для триграммного поиска (если еще не включено)
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        :param query: Строка поиска (минимум 2 символа)
        :param limit: Максимальное количество результатов
        :param threshold: Порог схожести для триграммного поиска (0-1)
        """
        if len(query) < 2:
            raise HTTPException(400, detail="Поисковый запрос должен содержать минимум 2 символа")
        
        search = f"%{query}%"
        
        # Комбинированный запрос
        stmt = (
            select(self.model)
            .where(
                or_(
                    func.lower(self.model.name) == func.lower(query),  # Точное совпадение
                    func.similarity(self.model.name, query) > threshold,  # Триграммный поиск
                    self.model.name.ilike(search)  # Простой поиск по подстроке
                )
            )
            .order_by(
                func.lower(self.model.name) == func.lower(query).desc(),  # Точные совпадения выше
                func.similarity(self.model.name, query).desc(),  # Сортировка по схожести
                self.model.name  # Альфавитный порядок для остальных
            )
            .limit(limit)
        )
        
        result = await self._session.execute(stmt)
        workouts = result.scalars().all()
        if not workouts:
            raise HTTPException(404, detail="Тренировки не найдены")
        
        return [WorkoutSearchItemResponse.model_validate(workout) for workout in workouts]
    

    async def get_daily_workouts_summary(
        self,
        user_id: int,
        target_date: date
    ) -> DailyWorkoutsSummaryResponse:
        """Возвращает сумму потраченных минут и каллорий за указанный день"""
        # Запрос для агрегации данных
        stmt = select(
        func.coalesce(func.sum(UserWorkout.duration_minutes), 0).label("total_duration"),
        func.coalesce(func.sum(UserWorkout.calories_burned), 0.0).label("total_calories_burned")
        ).where(
            and_(
                UserWorkout.user_id == user_id,
                UserWorkout.workout_date == target_date
            )
        )
        result = await self._session.execute(stmt)
        workout_data = result.mappings().one()
        return DailyWorkoutsSummaryResponse(**workout_data)
    

    async def get_daily_workouts(
        self,
        user_id: int,
        target_date: date
    ) -> DailyWorkoutsResponse:
        """Получает все упражнения за день"""
        stmt = (
            select(Workout.name, 
                UserWorkout.duration_minutes, 
                UserWorkout.calories_burned,
                Workout.description,
            )
            .join(Workout, UserWorkout.workout_id == Workout.id)
            .where(
                and_(
                    UserWorkout.user_id == user_id,
                    UserWorkout.workout_date == target_date
                )
            )
            .order_by(UserWorkout.id)  # Сохраняем порядок добавления
        )

        result = await self._session.execute(stmt)
        rows = result.all()
        if not rows:
            return DailyWorkoutsResponse(date=target_date, workouts=[])
        workouts = []
        for row in rows:
            # Проверяем, что все необходимые поля присутствуют
            name, duration_minutes, calories_burned, description = row
            if duration_minutes is None or calories_burned is None:
                logger.warning(
                    f"Пропущены данные для тренировки {name}: "
                    f"duration_minutes={duration_minutes}, calories_burned={calories_burned}"
                )
                continue  # Пропускаем некорректные записи

            workouts.append(
                WorkoutItemResponse(
                    name=name,
                    duration=duration_minutes,
                    calories=calories_burned,
                    description=description
                )
            )

        return DailyWorkoutsResponse(
            date=target_date,
            workouts=workouts
        )
    

    async def delete_workout_by_name_and_date(
        self,
        workout_name: str,
        workout_date: date,
        user_id: int,
    ) -> None:
        """Удаляет конкретную тренировку пользователя по названию и дате"""
        # Проверяем существование тренировки по имени
        stmt = select(Workout).where(func.lower(Workout.name) == func.lower(workout_name))
        result = await self._session.execute(stmt)
        workout = result.scalar_one_or_none()

        if not workout:
            raise HTTPException(404, detail=f"Тренировка с названием '{workout_name}' не найдена")

        # Удаляем запись из UserWorkout
        stmt = delete(UserWorkout).where(
            and_(
                UserWorkout.user_id == user_id,
                UserWorkout.workout_date == workout_date,
                UserWorkout.workout_id == workout.id
            )
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
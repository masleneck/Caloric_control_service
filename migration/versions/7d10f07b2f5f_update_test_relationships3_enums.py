"""update test relationships3(enums)

Revision ID: 7d10f07b2f5f
Revises: fe8ce5872332
Create Date: 2025-03-21 00:52:25.124525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7d10f07b2f5f'
down_revision: Union[str, None] = 'fe8ce5872332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Изменяем тип столбца birthday_date в profiles
    op.alter_column(
        'profiles', 'birthday_date',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        existing_nullable=True
    )

    # Изменяем тип столбца gender в testresults
    op.alter_column(
        'testresults', 'gender',
        existing_type=sa.VARCHAR(),
        type_=sa.Enum('MALE', 'FEMALE', 'NOT_STATED', name='gender'),
        postgresql_using='gender::text::gender',  # Явное преобразование данных
        nullable=False
    )

    # Изменяем тип столбца goal в testresults
    op.alter_column(
        'testresults', 'goal',
        existing_type=sa.VARCHAR(),
        type_=sa.Enum('LOSE_WEIGHT', 'KEEPING_FIT', 'GAIN_MUSCLE_MASS', 'NOT_STATED', name='currentgoal'),
        postgresql_using='goal::text::currentgoal',  # Явное преобразование данных
        nullable=False
    )


def downgrade() -> None:
    # Возвращаем тип столбца goal в testresults
    op.alter_column(
        'testresults', 'goal',
        existing_type=sa.Enum('LOSE_WEIGHT', 'KEEPING_FIT', 'GAIN_MUSCLE_MASS', 'NOT_STATED', name='currentgoal'),
        type_=sa.VARCHAR(),
        postgresql_using='goal::text',  # Явное преобразование данных
        nullable=True
    )

    # Возвращаем тип столбца gender в testresults
    op.alter_column(
        'testresults', 'gender',
        existing_type=sa.Enum('MALE', 'FEMALE', 'NOT_STATED', name='gender'),
        type_=sa.VARCHAR(),
        postgresql_using='gender::text',  # Явное преобразование данных
        nullable=True
    )

    # Возвращаем тип столбца birthday_date в profiles
    op.alter_column(
        'profiles', 'birthday_date',
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True
    )

    # Удаляем типы enum, если они больше не используются
    op.execute("DROP TYPE currentgoal")
    op.execute("DROP TYPE gender")
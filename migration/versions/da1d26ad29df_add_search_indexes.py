"""add_search_indexes

Revision ID: da1d26ad29df
Revises: 954d9e81fd18
Create Date: 2025-04-15 13:23:06.101395

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "da1d26ad29df"
down_revision: Union[str, None] = "954d9e81fd18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_index('ix_food_items_name_trgm', 'food_items', [sa.text('name gin_trgm_ops')], 
                   postgresql_using='gin')
    op.create_index('ix_food_items_name_lower', 'food_items', [sa.text('lower(name)')], 
                   postgresql_using='btree')


def downgrade() -> None:
    pass

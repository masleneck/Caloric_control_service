"""Изначальные таблицы созданы верно

Revision ID: 9e9e1f2ba0c8
Revises: 2d8897221615
Create Date: 2025-03-02 00:49:17.448953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e9e1f2ba0c8'
down_revision: Union[str, None] = '2d8897221615'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

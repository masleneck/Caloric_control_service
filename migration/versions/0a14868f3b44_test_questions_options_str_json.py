"""test_questions options str-> json

Revision ID: 0a14868f3b44
Revises: bdced3c48fcd
Create Date: 2025-03-14 00:54:52.196181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a14868f3b44'
down_revision: Union[str, None] = 'bdced3c48fcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'testquestions', 
        'options', 
        type_=sa.JSON, 
        postgresql_using='options::json'
    )

def downgrade():
    op.alter_column(
        'testquestions', 
        'options', 
        type_=sa.String, 
        postgresql_using='options::text'
    )
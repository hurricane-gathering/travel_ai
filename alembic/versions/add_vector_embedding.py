"""add vector embedding

Revision ID: add_vector_embedding
Revises: add_vector_indices
Create Date: 2024-03-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON

# revision identifiers, used by Alembic.
revision: str = 'add_vector_embedding'
down_revision: str = 'add_vector_indices'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 添加 vector_embedding 字段
    op.add_column(
        'spots',
        sa.Column('vector_embedding', JSON(), nullable=True)
    )

def downgrade() -> None:
    # 删除 vector_embedding 字段
    op.drop_column('spots', 'vector_embedding') 
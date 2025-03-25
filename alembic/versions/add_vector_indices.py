"""add vector indices

Revision ID: add_vector_indices
Revises: 
Create Date: 2024-03-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON

# revision identifiers, used by Alembic.
revision: str = 'add_vector_indices'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 创建索引
    op.create_index(
        'ix_vector_indices_collection_name',
        'vector_indices',
        ['collection_name']
    )
    op.create_index(
        'ix_vector_indices_record_id',
        'vector_indices',
        ['record_id']
    )

def downgrade() -> None:
    # 删除索引
    op.drop_index('ix_vector_indices_record_id')
    op.drop_index('ix_vector_indices_collection_name') 
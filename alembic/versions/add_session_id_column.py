"""add session_id column

Revision ID: add_session_id_column
Revises: add_chat_histories
Create Date: 2024-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_session_id_column'
down_revision: str = 'add_chat_histories'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 添加 session_id 列
    op.add_column('chat_histories', sa.Column('session_id', sa.String(), nullable=True))

def downgrade() -> None:
    # 删除 session_id 列
    op.drop_column('chat_histories', 'session_id') 
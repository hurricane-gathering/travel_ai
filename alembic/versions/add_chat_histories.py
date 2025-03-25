"""add chat histories

Revision ID: add_chat_histories
Revises: add_vector_embedding
Create Date: 2024-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_chat_histories'
down_revision: str = 'add_vector_embedding'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 创建聊天历史表
    op.create_table(
        'chat_histories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('user_query', sa.Text(), nullable=True),
        sa.Column('assistant_response', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # 删除聊天历史表
    op.drop_table('chat_histories') 
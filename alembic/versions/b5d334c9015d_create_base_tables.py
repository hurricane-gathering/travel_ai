"""create base tables

Revision ID: b5d334c9015d
Revises: add_vector_indices
Create Date: 2024-03-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import JSON

# revision identifiers, used by Alembic.
revision: str = 'b5d334c9015d'
down_revision: str = 'add_vector_indices'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 创建景点表
    op.create_table(
        'spots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('images', JSON(), nullable=True),
        sa.Column('tags', JSON(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('vector_embedding', JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建路线表
    op.create_table(
        'routes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('spots', JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

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

    # 创建向量索引表
    op.create_table(
        'vector_indices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('collection_name', sa.String(), nullable=True),
        sa.Column('record_id', sa.Integer(), nullable=True),
        sa.Column('vector', JSON(), nullable=True),
        sa.Column('meta_info', JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # 删除所有表
    op.drop_table('vector_indices')
    op.drop_table('chat_histories')
    op.drop_table('routes')
    op.drop_table('spots')

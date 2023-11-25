"""add table name user_purchases

Revision ID: 469f664d9524
Revises: f06a6d611f24
Create Date: 2023-11-25 12:45:25.209429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '469f664d9524'
down_revision: Union[str, None] = 'f06a6d611f24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_purchases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL"), nullable=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL"), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'])
    )


def downgrade() -> None:
    op.drop_table('user_purchases')
"""add product table

Revision ID: 209126abb3e3
Revises: 037284caf208
Create Date: 2023-11-22 12:04:17.992837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# This revision should be run third
# revision identifiers, used by Alembic.
revision: str = '209126abb3e3'
down_revision: Union[str, None] = '037284caf208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('stock_quantity', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('product_categories.id', ondelete="SET NULL"), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('products')

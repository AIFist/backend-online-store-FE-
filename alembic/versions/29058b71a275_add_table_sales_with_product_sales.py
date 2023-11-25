"""add table sales with product_sales

Revision ID: 29058b71a275
Revises: 1667e5e916c0
Create Date: 2023-11-25 11:07:35.622591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29058b71a275'
down_revision: Union[str, None] = '1667e5e916c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('discount_percent', sa.Float(), nullable=True),
        sa.Column('sale_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'product_sales',
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('sales_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['sales_id'], ['sales.id'], )
    )


def downgrade() -> None:
    op.drop_table('product_sales')
    op.drop_table('sales')


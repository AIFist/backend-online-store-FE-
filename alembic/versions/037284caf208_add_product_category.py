""" add Product Category

Revision ID: 037284caf208
Revises: 22d92581c905
Create Date: 2023-11-22 11:09:33.447435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '037284caf208'
down_revision: Union[str, None] = '22d92581c905'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(), nullable=True),
        sa.Column('parent_category_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['parent_category_id'], ['product_categories.id'], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('product_categories')

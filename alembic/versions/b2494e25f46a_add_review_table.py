"""add review table

Revision ID: b2494e25f46a
Revises: 209126abb3e3
Create Date: 2023-11-22 12:14:37.327553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# This revision should be run forth
# revision identifiers, used by Alembic.
revision: str = 'b2494e25f46a'
down_revision: Union[str, None] = '209126abb3e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL")),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL")),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('reviews')

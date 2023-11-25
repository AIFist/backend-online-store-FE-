""" add tables name carts and favorites

Revision ID: e78ffc5dc6be
Revises: cc9f61248cb6
Create Date: 2023-11-25 12:03:18.681453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = 'e78ffc5dc6be'
down_revision: Union[str, None] = 'cc9f61248cb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL")),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default="1"),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'favorites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL")),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('carts')
    op.drop_table('favorites')


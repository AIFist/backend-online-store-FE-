"""Add banners table

Revision ID: f99fe14f1f47
Revises: 31bd265848b1
Create Date: 2024-01-10 12:15:11.335470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f99fe14f1f47'
down_revision: Union[str, None] = '31bd265848b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'banners',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="CASCADE"), unique=True),
        # Add other columns as needed
    )


def downgrade() -> None:
    op.drop_table('banners')

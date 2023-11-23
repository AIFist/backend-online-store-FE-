"""add SKU column in the product table

Revision ID: 1667e5e916c0
Revises: 7cc911ffbeb8
Create Date: 2023-11-23 16:20:16.326009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1667e5e916c0'
down_revision: Union[str, None] = '7cc911ffbeb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('SKU', sa.String,nullable=True))



def downgrade() -> None:
    op.drop_column('products', 'SKU')

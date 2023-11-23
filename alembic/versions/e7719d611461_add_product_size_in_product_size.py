"""add product_size in product size

Revision ID: e7719d611461
Revises: 9f28ed173eb6
Create Date: 2023-11-23 11:37:06.114409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# on 7th number run this revision  7th
# revision identifiers, used by Alembic.
revision: str = 'e7719d611461'
down_revision: Union[str, None] = '9f28ed173eb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('product_size', sa.String, nullable=True))



def downgrade() -> None:
    op.drop_column('products', 'product_size')

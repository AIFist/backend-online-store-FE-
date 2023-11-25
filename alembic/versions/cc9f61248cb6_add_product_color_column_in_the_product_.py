""" add product_color column in the product table

Revision ID: cc9f61248cb6
Revises: 50e1ce7ecfdf
Create Date: 2023-11-25 11:33:17.729181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc9f61248cb6'
down_revision: Union[str, None] = '50e1ce7ecfdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('product_color', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('products', 'product_color')

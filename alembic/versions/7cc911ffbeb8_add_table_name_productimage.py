""" add table name ProductImage

Revision ID: 7cc911ffbeb8
Revises: ed82cad2a382
Create Date: 2023-11-23 15:50:21.330458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# this is 10 th
# revision identifiers, used by Alembic.
revision: str = '7cc911ffbeb8'
down_revision: Union[str, None] = 'ed82cad2a382'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('image_path', sa.String(), nullable=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL"),nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('product_images')

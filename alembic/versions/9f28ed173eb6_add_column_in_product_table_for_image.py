"""add column in product table for image

Revision ID: 9f28ed173eb6
Revises: 278a68c8aac0
Create Date: 2023-11-23 11:14:04.345030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision this is for adding images path in prodcut and run it on 6th number
# revision identifiers, used by Alembic.
revision: str = '9f28ed173eb6'
down_revision: Union[str, None] = '278a68c8aac0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('image_path', sa.String,nullable=True))


def downgrade() -> None:
    op.drop_column('products', 'image_path')

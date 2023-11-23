"""Drop image path column

Revision ID: ed82cad2a382
Revises: 185cb4bba492
Create Date: 2023-11-23 15:27:58.909398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# this is not importanta much
# revision identifiers, used by Alembic.
revision: str = 'ed82cad2a382'
down_revision: Union[str, None] = '185cb4bba492'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('products', 'image_path')


def downgrade() -> None:
    op.add_column('products', sa.Column('image_path', sa.String, nullable=True))

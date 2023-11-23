"""add column in product table named target_audience

Revision ID: 185cb4bba492
Revises: e7719d611461
Create Date: 2023-11-23 12:20:32.797861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# run this on 8th number 8
# revision identifiers, used by Alembic.
revision: str = '185cb4bba492'
down_revision: Union[str, None] = 'e7719d611461'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('target_audience', sa.String,nullable=True))



def downgrade() -> None:
    op.drop_column('products','target_audience')

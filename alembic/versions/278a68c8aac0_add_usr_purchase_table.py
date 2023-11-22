"""add usr purchase table 

Revision ID: 278a68c8aac0
Revises: b2494e25f46a
Create Date: 2023-11-22 12:26:27.681716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '278a68c8aac0'
down_revision: Union[str, None] = 'b2494e25f46a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_purchase',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL"))
    )



def downgrade() -> None:
    op.drop_table('user_purchase')

"""drop user purchase

Revision ID: f06a6d611f24
Revises: e78ffc5dc6be
Create Date: 2023-11-25 12:30:21.407842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f06a6d611f24'
down_revision: Union[str, None] = 'e78ffc5dc6be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('user_purchase')


def downgrade() -> None:
    op.create_table(
        'user_purchase',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="SET NULL")),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete="SET NULL"))
    )

""" add column spiing and bliing in user table

Revision ID: 50e1ce7ecfdf
Revises: 29058b71a275
Create Date: 2023-11-25 11:23:06.467128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50e1ce7ecfdf'
down_revision: Union[str, None] = '29058b71a275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('billing_address', sa.String(), nullable=True))
    op.add_column('users', sa.Column('shipping_address', sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_column('users', 'shipping_address')
    op.drop_column('users', 'billing_address')
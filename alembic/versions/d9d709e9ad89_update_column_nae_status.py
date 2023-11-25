""" update column nae status 

Revision ID: d9d709e9ad89
Revises: 469f664d9524
Create Date: 2023-11-25 12:57:37.016653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9d709e9ad89'
down_revision: Union[str, None] = '469f664d9524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user_purchases', 'status', server_default='pending')



def downgrade() -> None:
    pass

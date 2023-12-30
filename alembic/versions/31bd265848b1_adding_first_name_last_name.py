"""adding first name last name

Revision ID: 31bd265848b1
Revises: efcbbf31b8a4
Create Date: 2023-12-30 13:21:40.418103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31bd265848b1'
down_revision: Union[str, None] = 'efcbbf31b8a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))



def downgrade() -> None:
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
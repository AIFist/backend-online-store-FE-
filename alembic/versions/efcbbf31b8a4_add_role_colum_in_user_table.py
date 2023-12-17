"""add role colum in user table

Revision ID: efcbbf31b8a4
Revises: 0fb8e434ab7b
Create Date: 2023-12-17 10:45:39.418537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efcbbf31b8a4'
down_revision: Union[str, None] = '0fb8e434ab7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'role')

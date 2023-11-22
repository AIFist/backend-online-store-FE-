"""Add user table

Revision ID: 22d92581c905
Revises: 
Create Date: 2023-11-22 11:05:31.336964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, text

# revision identifiers, used by Alembic.
revision: str = '22d92581c905'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('users')

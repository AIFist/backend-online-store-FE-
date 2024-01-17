"""Create Token table

Revision ID: 749675d83296
Revises: f99fe14f1f47
Create Date: 2024-01-17 13:11:43.864947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '749675d83296'
down_revision: Union[str, None] = 'f99fe14f1f47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="CASCADE"), index=True, nullable=False),
        sa.Column('token', sa.String(), index=True, unique=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('tokens')

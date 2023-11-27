"""alter price column in product table

Revision ID: ece97caf5075
Revises: d9d709e9ad89
Create Date: 2023-11-27 13:27:50.516261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ece97caf5075'
down_revision: Union[str, None] = 'd9d709e9ad89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the datatype of the 'price' column from Integer to Float
    op.alter_column('products', 'price', type_=sa.Float)



def downgrade() -> None:
    # In case of rollback, revert the changes
    op.alter_column('products', 'price', type_=sa.Integer)


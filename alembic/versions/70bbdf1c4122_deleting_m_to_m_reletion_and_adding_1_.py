"""deleting m to m reletion and adding 1 to 1 

Revision ID: 70bbdf1c4122
Revises: ece97caf5075
Create Date: 2023-12-03 12:07:44.375709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70bbdf1c4122'
down_revision: Union[str, None] = 'ece97caf5075'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add a new column 'product_id' to the 'sales' table
    op.add_column('sales', sa.Column('product_id', sa.Integer(), nullable=True))

    # Create a foreign key constraint on the 'product_id' column
    op.create_foreign_key('fk_sales_product', 'sales', 'products', ['product_id'], ['id'], ondelete='SET NULL')

    # Drop the existing many-to-many relationship table 'product_sales_association'
    op.drop_table('product_sales')



def downgrade() -> None:
    # Recreate the many-to-many relationship table 'product_sales'
    op.create_table(
        'product_sales',
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id')),
        sa.Column('sales_id', sa.Integer(), sa.ForeignKey('sales.id'))
    )

    # Remove the foreign key constraint and the 'product_id' column from the 'sales' table
    op.drop_constraint('fk_sales_product', 'sales', type_='foreignkey')
    op.drop_column('sales', 'product_id')


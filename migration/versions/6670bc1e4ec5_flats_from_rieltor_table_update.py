"""Flats from rieltor table update

Revision ID: 6670bc1e4ec5
Revises: 1cf15113bce1
Create Date: 2025-03-24 13:16:48.304188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6670bc1e4ec5'
down_revision: Union[str, None] = '1cf15113bce1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Flats_from_rieltor', sa.Column('photos', sa.JSON(), nullable=True))
    op.create_unique_constraint(None, 'Flats_from_rieltor', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Flats_from_rieltor', type_='unique')
    op.drop_column('Flats_from_rieltor', 'photos')
    # ### end Alembic commands ###

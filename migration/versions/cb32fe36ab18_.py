"""empty message

Revision ID: cb32fe36ab18
Revises: 7eb0df44db45
Create Date: 2025-05-12 19:03:20.565098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb32fe36ab18'
down_revision: Union[str, None] = '7eb0df44db45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=True),
    sa.Column('total_floors', sa.Integer(), nullable=True),
    sa.Column('area', sa.Float(), nullable=False),
    sa.Column('living_area', sa.Float(), nullable=True),
    sa.Column('kitchen_area', sa.Float(), nullable=True),
    sa.Column('year_built', sa.Integer(), nullable=True),
    sa.Column('building_type', sa.String(), nullable=True),
    sa.Column('condition', sa.String(), nullable=True),
    sa.Column('has_balcony', sa.Boolean(), nullable=True),
    sa.Column('is_furnished', sa.Boolean(), nullable=True),
    sa.Column('listed_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('seller_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['seller_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apartments')
    # ### end Alembic commands ###

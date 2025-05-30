"""update migration

Revision ID: 53a9ca116c13
Revises: dff21ca8a375
Create Date: 2025-03-24 17:00:18.244596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53a9ca116c13'
down_revision: Union[str, None] = 'dff21ca8a375'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'subscription', ['id'])
    op.create_unique_constraint(None, 'user_subscription', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'user_subscription', type_='unique')
    op.drop_constraint(None, 'subscription', type_='unique')
    # ### end Alembic commands ###

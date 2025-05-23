"""Create

Revision ID: b479a1e3d057
Revises: cd7bf2735aec
Create Date: 2025-05-12 16:59:43.866904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b479a1e3d057'
down_revision: Union[str, None] = 'cd7bf2735aec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipments', sa.Column('equipmentorders_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'equipments', 'equipmentorders', ['equipmentorders_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'equipments', type_='foreignkey')
    op.drop_column('equipments', 'equipmentorders_id')
    # ### end Alembic commands ###

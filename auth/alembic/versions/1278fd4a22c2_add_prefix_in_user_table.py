"""add prefix in user table

Revision ID: 1278fd4a22c2
Revises: ce66c1f7c8d2
Create Date: 2023-09-05 14:55:55.737371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1278fd4a22c2'
down_revision: Union[str, None] = 'ce66c1f7c8d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('prefix', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'prefix')
    # ### end Alembic commands ###

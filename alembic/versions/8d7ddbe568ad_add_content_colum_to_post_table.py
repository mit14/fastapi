"""add content colum to post table

Revision ID: 8d7ddbe568ad
Revises: dbd46d646850
Create Date: 2024-05-12 16:07:27.565054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d7ddbe568ad'
down_revision: Union[str, None] = 'dbd46d646850'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    pass

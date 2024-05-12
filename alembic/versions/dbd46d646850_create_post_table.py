"""create post table

Revision ID: dbd46d646850
Revises: 
Create Date: 2024-05-12 15:54:07.395036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbd46d646850'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True,), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')   # need to provide the command to drop the table if that didnt work out properly. 
    pass

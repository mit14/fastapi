"""add foreign key to post taqble

Revision ID: 14fbb72e74cd
Revises: 4147c83ec81c
Create Date: 2024-05-12 16:23:40.741733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14fbb72e74cd'
down_revision: Union[str, None] = '4147c83ec81c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='post', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='post')
    op.drop_column('post','owner_id')
    pass

"""add last few columns in post table

Revision ID: 0eb8281449e0
Revises: 14fbb72e74cd
Create Date: 2024-05-12 16:43:13.328509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb8281449e0'
down_revision: Union[str, None] = '14fbb72e74cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
                  
    pass


def downgrade() -> None:
    op.drop_column('post', 'created_at')
    op.drop_column('post', 'published')
    pass

"""deleted_created_at

Revision ID: fa293d7714fa
Revises: ffc8666896d2
Create Date: 2024-08-16 22:32:20.364117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa293d7714fa'
down_revision: Union[str, None] = 'ffc8666896d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Categories', 'type')
    op.drop_column('Tasks', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('created_at', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('Categories', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

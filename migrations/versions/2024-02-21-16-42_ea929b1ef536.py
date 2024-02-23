"""add body_param_schema to action

Revision ID: ea929b1ef536
Revises: 3b58937fb542
Create Date: 2024-02-21 16:42:17.914532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ea929b1ef536'
down_revision: Union[str, None] = '3b58937fb542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('action', sa.Column('body_param_schema', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('action', 'body_param_schema')
    # ### end Alembic commands ###
"""Add date_formed field to the Band model

Revision ID: 8046941a0134
Revises: d512ec505aac
Create Date: 2024-07-22 11:16:29.658870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8046941a0134'
down_revision: Union[str, None] = 'd512ec505aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('band', sa.Column('date_formed', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('band', 'date_formed')
    # ### end Alembic commands ###

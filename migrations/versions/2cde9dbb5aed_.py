"""empty message

Revision ID: 2cde9dbb5aed
Revises: c105c5f1f97e
Create Date: 2019-10-28 18:45:27.354047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cde9dbb5aed'
down_revision = 'c105c5f1f97e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movielist', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'create_time')
    op.drop_column('movielist', 'create_time')
    # ### end Alembic commands ###
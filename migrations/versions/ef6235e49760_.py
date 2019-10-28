"""empty message

Revision ID: ef6235e49760
Revises: c8bca7a170bf
Create Date: 2019-10-28 18:50:51.733283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef6235e49760'
down_revision = 'c8bca7a170bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movielist',
    sa.Column('rating', sa.String(length=100), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('cover_url', sa.String(length=100), nullable=False),
    sa.Column('is_playable', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=50), autoincrement=False, nullable=False),
    sa.Column('types', sa.String(length=100), nullable=False),
    sa.Column('regions', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('release_date', sa.String(length=100), nullable=False),
    sa.Column('actor_count', sa.String(length=100), nullable=False),
    sa.Column('vote_count', sa.String(length=100), nullable=False),
    sa.Column('score', sa.String(length=100), nullable=False),
    sa.Column('actors', sa.String(length=500), nullable=False),
    sa.Column('is_watched', sa.Boolean(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movielist')
    # ### end Alembic commands ###

"""add videos table and videos column to users table

Revision ID: 07bec9045e6e
Revises: 438c9388929f
Create Date: 2022-04-15 15:28:13.687256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07bec9045e6e'
down_revision = '438c9388929f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('videos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('video_path', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos')
    # ### end Alembic commands ###
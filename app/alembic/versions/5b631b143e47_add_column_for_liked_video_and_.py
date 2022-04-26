"""add column for liked video and followers with following

Revision ID: 5b631b143e47
Revises: 9bed272850b1
Create Date: 2022-04-26 21:20:53.033182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b631b143e47'
down_revision = '9bed272850b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    op.create_table('liked_video',
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], )
    )
    op.drop_column('users', 'subscribers_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('subscribers_count', sa.INTEGER(), nullable=True))
    op.drop_table('liked_video')
    op.drop_table('followers')
    # ### end Alembic commands ###

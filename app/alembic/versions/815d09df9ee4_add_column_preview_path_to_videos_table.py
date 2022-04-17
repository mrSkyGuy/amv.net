"""add column preview_path to videos table

Revision ID: 815d09df9ee4
Revises: 
Create Date: 2022-04-16 19:00:57.323426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815d09df9ee4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('preview_path', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'preview_path')
    # ### end Alembic commands ###
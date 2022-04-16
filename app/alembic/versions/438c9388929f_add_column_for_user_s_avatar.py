"""Add column for user's avatar

Revision ID: 438c9388929f
Revises: 
Create Date: 2022-04-14 16:04:29.149801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '438c9388929f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_image')
    # ### end Alembic commands ###
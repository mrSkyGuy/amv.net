"""set unique and index for username field in users table

Revision ID: 92922d95d7b5
Revises: 07bec9045e6e
Create Date: 2022-04-15 21:30:55.260673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92922d95d7b5'
down_revision = '07bec9045e6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    # ### end Alembic commands ###

"""Initial migration.

Revision ID: fd4563276880
Revises: 04c0da7c77c2
Create Date: 2022-02-01 18:44:14.886526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd4563276880'
down_revision = '04c0da7c77c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scores', sa.Column('replied', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scores', 'replied')
    # ### end Alembic commands ###

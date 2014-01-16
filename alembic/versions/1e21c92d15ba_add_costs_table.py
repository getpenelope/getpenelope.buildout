"""add costs table

Revision ID: 1e21c92d15ba
Revises: 2560e7175da8
Create Date: 2014-01-15 17:24:42.156487

"""

# revision identifiers, used by Alembic.
revision = '1e21c92d15ba'
down_revision = '2560e7175da8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('costs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(precision=2), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('costs')
    ### end Alembic commands ###

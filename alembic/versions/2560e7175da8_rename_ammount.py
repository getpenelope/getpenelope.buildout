"""rename_ammount

Revision ID: 2560e7175da8
Revises: 38914e68d30f
Create Date: 2013-12-23 13:18:17.683670

"""

# revision identifiers, used by Alembic.
revision = '2560e7175da8'
down_revision = '38914e68d30f'

from alembic import op


def upgrade():
    op.alter_column('contracts', 'ammount', new_column_name='amount')


def downgrade():
    op.alter_column('contracts', 'amount', new_column_name='ammount')

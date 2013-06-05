"""commessa

Revision ID: 538e6ad6eadb
Revises: 570b3a41fca9
Create Date: 2013-06-04 14:25:00.809483

"""

# revision identifiers, used by Alembic.
revision = '538e6ad6eadb'
down_revision = '570b3a41fca9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
                    'contracts',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('name', sa.Unicode(length=None), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=True),
                    sa.Column('workflow_state', sa.Unicode(length=None), nullable=True),
                    sa.Column('contract_number', sa.Unicode(length=None), nullable=True),
                    sa.Column('modification_date', sa.DateTime(timezone=False), nullable=True),
                    sa.Column('days', sa.Float(precision=2, asdecimal=False), nullable=True),
                    sa.Column('ammount', sa.Float(precision=2, asdecimal=False), nullable=True),
                    sa.Column('creation_date', sa.DateTime(timezone=False), nullable=True),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.Column('project_id', sa.String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), nullable=False),
                    sa.Column('start_date', sa.Date(), nullable=True),
                    sa.Column('description', sa.Unicode(length=None), nullable=True),
                    sa.PrimaryKeyConstraint(u'id', name=u'contracts_pkey')
                    )

    op.alter_column('contracts', u'id', 
               existing_type=sa.INTEGER(), 
               type_=sa.String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False), 
               existing_nullable=False, 
               existing_server_default='''nextval('contracts_id_seq'::regclass)''')
    op.alter_column('customer_requests', u'contract', new_column_name='old_contract_name')
    op.add_column('customer_requests', sa.Column('contract_id', sa.String(), nullable=True))


def downgrade():
    op.drop_table('contracts')
    op.alter_column('customer_requests', u'old_contract_name', new_column_name='contract')
    op.drop_column('customer_requests', 'contract_id')

"""activity stream

Revision ID: 2085e29b4e7f
Revises: 4d2343e82c45
Create Date: 2014-01-31 13:51:53.797025

"""

# revision identifiers, used by Alembic.
revision = '2085e29b4e7f'
down_revision = '4d2343e82c45'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
                    'activities',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('message', sa.Unicode(length=None), nullable=True),
                    sa.Column('created_by', sa.String(), nullable=True),
                    sa.Column('absolute_path', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=False), nullable=True, index=True),
                    sa.Column('seen_at', sa.DateTime(timezone=False), nullable=True, index=True),
                    sa.Column('read_at', sa.DateTime(timezone=False), nullable=True, index=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint(u'id', name=u'activities_pkey')
                    )
    op.alter_column('activities', u'id', 
               existing_type=sa.INTEGER(), 
               type_=sa.Integer(),
               existing_nullable=False, 
               existing_server_default='''nextval('activities_id_seq'::regclass)''')


def downgrade():
    op.drop_table('activities')

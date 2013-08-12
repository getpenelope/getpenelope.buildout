"""kanbanboard

Revision ID: 275c8091ee37
Revises: 483950e462cf
Create Date: 2013-06-27 15:57:26.207511

"""

# revision identifiers, used by Alembic.
revision = '275c8091ee37'
down_revision = '483950e462cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
                    'kanban_boards',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('name', sa.Unicode(length=None), nullable=True),
                    sa.Column('json', sa.Unicode(), nullable=True),
                    sa.Column('modification_date', sa.DateTime(timezone=False), nullable=True),
                    sa.Column('creation_date', sa.DateTime(timezone=False), nullable=True),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint(u'id', name=u'kanban_boards_pkey')
                    )

    op.alter_column('kanban_boards', u'id', 
               existing_type=sa.INTEGER(), 
               type_=sa.Integer(),
               existing_nullable=False, 
               existing_server_default='''nextval('kanban_boards_id_seq'::regclass)''')


def downgrade():
    op.drop_table('kanban_boards')

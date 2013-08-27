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
                    sa.Column('board_query', sa.Unicode(), nullable=True),
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

    op.create_table('kanban_projects',
                    sa.Column('project_id', sa.String(), sa.ForeignKey('projects.id', ondelete="CASCADE")),
                    sa.Column('kanban_id', sa.Integer(), sa.ForeignKey('kanban_boards.id', ondelete="CASCADE")),
                    )
    op.add_column('kanban_boards', sa.Column('backlog_limit', sa.Integer(), nullable=False))
    op.add_column('kanban_boards', sa.Column('backlog_order', sa.Unicode(), nullable=False))
    op.add_column('kanban_boards', sa.Column('backlog_query', sa.Unicode(), nullable=True))
    op.drop_column('kanban_boards', u'board_query')
    op.alter_column('kanban_boards', u'name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    op.create_table('kanban_acl',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('principal', sa.String(), nullable=True),
            sa.Column('permission_name', sa.String(), nullable=True),
            sa.Column('board_id', sa.Integer(), sa.ForeignKey('kanban_boards.id', ondelete="CASCADE")),
            sa.PrimaryKeyConstraint('id')
            )

def downgrade():
    op.drop_table('kanban_acl')
    op.drop_table('kanban_projects')
    op.drop_table('kanban_boards')

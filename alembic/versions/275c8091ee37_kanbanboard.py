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
                    sa.Column('project_id', sa.String(), sa.ForeignKey('projects.id')),
                    sa.Column('kanban_id', sa.Integer(), sa.ForeignKey('kanban_boards.id')),
                    )

    op.create_table(
                    'kanban_acl',
                    sa.Column('board_id', sa.Integer(), sa.ForeignKey('kanban_boards.id'), primary_key=True, nullable=False),
                    sa.Column('principal', sa.String(), primary_key=True, nullable=False),
                    sa.Column('permission_name', sa.String(), primary_key=True, nullable=False),
                    sa.PrimaryKeyConstraint(u'board_id', u'principal', u'permission_name', name=u'kanban_acl_pkey')
                    )

    op.alter_column('kanban_acl', u'board_id', 
               existing_type=sa.INTEGER(), 
               type_=sa.Integer(),
               existing_nullable=False, 
               existing_server_default='''nextval('kanban_acl_board_id_seq'::regclass)''')

    op.alter_column('kanban_acl', u'principal', 
               existing_nullable=False, 
               existing_server_default='''nextval('kanban_acl_principal_seq'::regclass)''')

    op.alter_column('kanban_acl', u'permission_name', 
               existing_nullable=False, 
               existing_server_default='''nextval('kanban_acl_permission_name_seq'::regclass)''')

def downgrade():
    op.drop_table('kanban_acl')
    op.drop_table('kanban_projects')
    op.drop_table('kanban_boards')

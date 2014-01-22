"""add update cascade

Revision ID: 47fb94ed7f66
Revises: 1e21c92d15ba
Create Date: 2014-01-22 08:48:30.293303

"""

# revision identifiers, used by Alembic.
revision = '47fb94ed7f66'
down_revision = '1e21c92d15ba'

from alembic import op
from penelope.core.models import DBSession
import transaction


def upgrade():
    context = op.get_context()
    DBSession().bind = context.bind
    DBSession().execute(
    """ALTER TABLE applications DROP CONSTRAINT "applications_project_id_fkey", ADD CONSTRAINT "applications_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;
       ALTER TABLE customer_requests DROP CONSTRAINT "customer_requests_project_id_fkey", ADD CONSTRAINT "customer_requests_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;
       ALTER TABLE groups DROP CONSTRAINT "groups_project_id_fkey", ADD CONSTRAINT "groups_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;
       ALTER TABLE contracts ADD CONSTRAINT "contracts_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;
       ALTER TABLE kanban_projects DROP CONSTRAINT "kanban_projects_project_id_fkey", ADD CONSTRAINT "kanban_projects_project_id_fkey" foreign key (project_id) references projects(id) on update cascade on delete cascade;
       ALTER TABLE favorite_projects DROP CONSTRAINT "favorite_projects_project_id_fkey", ADD CONSTRAINT "favorite_projects_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;
       ALTER TABLE time_entries DROP CONSTRAINT "time_entries_project_id_fkey", ADD CONSTRAINT "time_entries_project_id_fkey" foreign key (project_id) references projects(id) on update cascade;""")
    transaction.commit()


def downgrade():
    pass

"""kanbanboard json upgrade

Revision ID: 4d2343e82c45
Revises: 2ef36286d521
Create Date: 2014-01-29 17:02:54.361794

"""

# revision identifiers, used by Alembic.
revision = '4d2343e82c45'
down_revision = '2ef36286d521'

import transaction
from json import dumps, loads
from alembic import op
from penelope.core.models import DBSession
from penelope.core.models.dashboard import KanbanBoard


def update_id(id_):
    if id_.find('#') > 0:
        return id_
    li = id_.rsplit('_', 1)
    return '#'.join(li)


def upgrade():
    context = op.get_context()
    DBSession().bind = context.bind

    for b in DBSession().query(KanbanBoard):
        if b.json:
            columns = loads(b.json)
            for n, column in enumerate(columns):
                for m, task in enumerate(column['tasks']):
                    new_id = update_id(task['id'])
                    print task['id'], new_id
                    if new_id != task['id']:
                        columns[n]['tasks'][m]['id'] = new_id
                        b.json = dumps(columns)
    transaction.commit()

def downgrade():
    pass

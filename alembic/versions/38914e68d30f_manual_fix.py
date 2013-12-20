"""manual_fix

Revision ID: 38914e68d30f
Revises: 59ac06532ad4
Create Date: 2013-12-20 09:46:34.439525

"""

# revision identifiers, used by Alembic.
revision = '38914e68d30f'
down_revision = '59ac06532ad4'

from alembic import op
from penelope.core.models import DBSession
from penelope.core.models.tp import TimeEntry
import transaction

def upgrade():
    context = op.get_context()
    DBSession().bind = context.bind
    for tp in DBSession().query(TimeEntry).filter_by(customer_request_id=None):
        for trac in tp.project.tracs:
            cr = DBSession().execute('select value from "trac_%s".ticket_custom where name=\'customerrequest\' and ticket=%s' % (trac.trac_name, tp.ticket)).fetchone()
            sql_cr = DBSession().execute('select id from customer_requests where id=\'%s\'' % cr.value).fetchone()
            tp.customer_request_id = sql_cr.id
            print sql_cr.id
    transaction.commit()

def downgrade():
    pass

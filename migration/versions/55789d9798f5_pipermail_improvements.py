"""pipermail-improvements

Revision ID: 55789d9798f5
Revises: d0578a57e0f9
Create Date: 2018-05-27 07:56:34.227078

"""

# revision identifiers, used by Alembic.
revision = '55789d9798f5'
down_revision = 'd0578a57e0f9'

import sqlalchemy as sa
from alembic import op
from depot.fields.sqlalchemy import UploadedFileField


def upgrade():
    op.create_table(
        'mailattachments',
        sa.Column('id',
            sa.Integer,
            autoincrement=True,
            primary_key=True),
        sa.Column('message_id',
            sa.Unicode,
            sa.ForeignKey('mailmessages.message_id')),
        sa.Column('file', UploadedFileField))
    op.execute(sa.table('mailmessages').delete())


def downgrade():
    op.execute(sa.table('mailmessages').delete())
    op.drop_table('mailattachments')

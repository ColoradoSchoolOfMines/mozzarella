"""
presentations

Revision ID: f8fa04b0714d
Revises: 36e3bdae7eab
Create Date: 2018-11-25 23:27:40.847593

"""

from alembic import op
import sqlalchemy as sa
from depot.fields.sqlalchemy import UploadedFileField

# revision identifiers, used by Alembic.
revision = 'f8fa04b0714d'
down_revision = '36e3bdae7eab'


def upgrade():
    op.create_table(
        'presentation',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('tarball', UploadedFileField),
    )

    op.create_table(
        'presentation_author_user',
        sa.Column('presentation_id',
                  sa.Integer,
                  sa.ForeignKey('presentation.id'),
                  primary_key=True),
        sa.Column('user_id',
                  sa.Integer,
                  sa.ForeignKey('tg_user.user_id'),
                  primary_key=True),
    )


def downgrade():
    op.drop_table('presentation')
    op.drop_table('presentation_author_user')

"""
Profile page field additions

Revision ID: 36e3bdae7eab
Revises: 55789d9798f5
Create Date: 2018-08-19 22:27:25.322273

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36e3bdae7eab'
down_revision = '55789d9798f5'

new_columns = ('bio', 'github_username', 'tagline')


def upgrade():
    for f in new_columns:
        op.add_column('tg_user', sa.Column(f, sa.Unicode(256), nullable=True))


def downgrade():
    for f in new_columns:
        op.drop_column('tg_user', f)

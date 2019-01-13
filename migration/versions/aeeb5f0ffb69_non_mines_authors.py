"""
Non-Mines authors

Revision ID: aeeb5f0ffb69
Revises: 92209b31e50a
Create Date: 2019-01-12 17:53:10.578059

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aeeb5f0ffb69'
down_revision = '92209b31e50a'


def upgrade():
    op.add_column(
        'presentation',
        sa.Column('_other_authors', sa.Unicode(512)),
    )


def downgrade():
    op.drop_column('presentation', '_other_authors')

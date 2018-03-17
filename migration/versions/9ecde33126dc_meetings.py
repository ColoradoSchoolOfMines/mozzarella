"""Meetings Schema

Revision ID: 9ecde33126dc
Revises: None
Create Date: 2017-08-05 15:00:32.788072

"""

# revision identifiers, used by Alembic.
revision = '9ecde33126dc'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'meeting',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('location', sa.Text()),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('description', sa.Unicode())
    )


def downgrade():
    op.drop_table('meeting')

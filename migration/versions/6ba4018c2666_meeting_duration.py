"""meeting duration

Revision ID: 6ba4018c2666
Revises: 5e0acc98a818
Create Date: 2017-10-10 19:02:42.165459

"""

# revision identifiers, used by Alembic.
revision = '6ba4018c2666'
down_revision = '5e0acc98a818'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'meeting',
        sa.Column('_duration', sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_column('meeting', '_duration')

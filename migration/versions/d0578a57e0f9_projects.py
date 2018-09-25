"""Projects Schema

Revision ID: d0578a57e0f9
Revises: bbd3bba567c1
Create Date: 2017-12-15 22:15:07.284502

Modified 2018-04-23 as the previous version was totally broken.
You must create a table before it's foreign key relations...

"""

# revision identifiers, used by Alembic.
revision = 'd0578a57e0f9'
down_revision = 'bbd3bba567c1'

from alembic import op
import sqlalchemy as sa

from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Unicode(1024), nullable=False),
        sa.Column('description', sa.Unicode(4096)),
        sa.Column('website', sa.Unicode(512)),
        sa.Column('repository', sa.Unicode(512)),
        sa.Column('video_url', sa.Unicode(512)),
        sa.Column('image', UploadedFileField(upload_type=UploadedImageWithThumb)))

    # Team XREF table
    op.create_table(
        'team',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('tg_user.user_id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.UniqueConstraint('user_id', 'project_id'))


def downgrade():
    op.drop_table('team')
    op.drop_table('projects')

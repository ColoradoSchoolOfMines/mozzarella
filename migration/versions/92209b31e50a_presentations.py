"""
Presentations

Revision ID: 92209b31e50a
Revises: 36e3bdae7eab
Create Date: 2019-01-02 16:22:15.746372

"""

from alembic import op
import sqlalchemy as sa
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb

# revision identifiers, used by Alembic.
revision = '92209b31e50a'
down_revision = '36e3bdae7eab'


def upgrade():
    op.create_table(
        'presentation',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(32), nullable=False),
        sa.Column('description', sa.Unicode),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('thumbnail',
                  UploadedFileField(upload_type=UploadedImageWithThumb)),
        sa.Column('repo_url', sa.Unicode(512)),
    )

    op.create_table(
        'presentation_author',
        sa.Column('presentation_id', sa.Integer, sa.ForeignKey('presentation.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('tg_user.user_id'), primary_key=True),
    )

    op.create_table(
        'presentation_file',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('presentation_id', sa.Integer, sa.ForeignKey('presentation.id'), nullable=False),
        sa.Column('description', sa.String(32), nullable=False),
        sa.Column('file', UploadedFileField, nullable=False),
    )


def downgrade():
    op.drop_table('presentation')
    op.drop_table('presentation_author')
    op.drop_table('presentation_file')

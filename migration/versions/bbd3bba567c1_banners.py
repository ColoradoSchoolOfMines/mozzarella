"""Banners

Revision ID: bbd3bba567c1
Revises: 6ba4018c2666
Create Date: 2017-12-16 02:51:54.685902

"""

# revision identifiers, used by Alembic.
revision = 'bbd3bba567c1'
down_revision = '6ba4018c2666'

from alembic import op
import sqlalchemy as sa
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb


def upgrade():
    op.create_table(
        'banner',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('photo',
                  UploadedFileField(upload_type=UploadedImageWithThumb)),
        sa.Column('description', sa.Unicode(2048), unique=True)
    )


def downgrade():
    op.drop_table('banner')

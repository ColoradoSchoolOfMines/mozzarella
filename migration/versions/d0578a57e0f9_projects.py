"""Projects Schema

Revision ID: d0578a57e0f9
Revises: 6ba4018c2666
Create Date: 2017-12-15 22:15:07.284502

"""

# revision identifiers, used by Alembic.
revision = 'd0578a57e0f9'
down_revision = '6ba4018c2666'

from alembic import op
import sqlalchemy as sa

from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb


def upgrade():
    # Add the Team XREF table
    op.create_table(
        'team',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('tg_user.user_id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
        sa.UniqueConstraint('user_id', 'project_id'),
    )

    # Create the actual projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Unicode(1024), nullable=False),
        sa.Column('description', sa.Unicode(4096)),
        sa.Column('website', sa.Unicode(512)),
        sa.Column('repository', sa.Unicode(512)),
        sa.Column('status', sa.Unicode(1), nullable=False, default="u"),
        sa.Column('reject_reason', sa.Unicode(512)),
        sa.Column('image', UploadedFileField(upload_type=UploadedImageWithThumb)),

        # Ensure that the statu is valid.
        # u -> unverified, r-> rejected, v->verified
        sa.CheckConstraint("status in ('u', 'r', 'v')"),

        # Require reject reason if project is rejected
        sa.CheckConstraint("reject_reason is not null or status != 'r'")
    )


def downgrade():
    op.drop_table('team')
    op.drop_table('projects')

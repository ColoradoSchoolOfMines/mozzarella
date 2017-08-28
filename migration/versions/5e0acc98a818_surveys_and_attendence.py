"""Surveys and attendence

Revision ID: 5e0acc98a818
Revises: 9ecde33126dc
Create Date: 2017-08-23 11:20:49.749277

"""

# revision identifiers, used by Alembic.
revision = '5e0acc98a818'
down_revision = '9ecde33126dc'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        'meeting',
        sa.Column('survey_id', sa.Integer, unique=True),
    )

    op.create_table(
        'survey',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('opens', sa.DateTime),
        sa.Column('closes', sa.DateTime),
    )

    op.create_table(
        'field',
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("type", sa.String(255), nullable=False),
        sa.Column("priority", sa.Float, default=0),
        sa.Column("name", sa.String(255), unique=True, nullable=False),
        sa.Column("label", sa.Unicode),
        sa.Column("required", sa.Boolean, default=False),
        sa.Column("first_time", sa.Boolean, default=False),
        sa.Column("placeholder", sa.Unicode),
        sa.Column("value", sa.Unicode),
        sa.Column("options", sa.Unicode),
        sa.Column("min", sa.Float),
        sa.Column("max", sa.Float),
        sa.Column("step", sa.Float),
    )

    op.create_table(
        'survey_field',
        sa.Column('survey_id', sa.Integer, sa.ForeignKey('survey.id'), primary_key=True),
        sa.Column('field_id', sa.Integer, sa.ForeignKey('field.id'), primary_key=True),
    )

    op.create_table(
        'response',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('tg_user.user_id')),
        sa.Column('provided_name', sa.Unicode(255)),
        sa.Column('survey_id', sa.Integer, sa.ForeignKey('survey.id'), nullable=False),
    )

    op.create_table(
        'response_data',
        sa.Column('response_id', sa.Integer, sa.ForeignKey('response.id'), primary_key=True, nullable=False),
        sa.Column('field_id', sa.Integer, sa.ForeignKey('field.id'), primary_key=True, nullable=False),
        sa.Column('contents', sa.Unicode, nullable=False),
    )


def downgrade():
    op.drop_table('response_data')
    op.drop_table('response')
    op.drop_table('survey_field')
    op.drop_table('field')
    op.drop_table('survey')
    op.drop_column('meeting', 'survey_id')
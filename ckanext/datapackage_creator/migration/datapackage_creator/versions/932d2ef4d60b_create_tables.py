"""create tables

Revision ID: 932d2ef4d60b
Revises:
Create Date: 2022-12-28 08:26:18.535734

"""
import uuid
import datetime as dt
import sqlalchemy as sa

from alembic import op

from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = '932d2ef4d60b'
down_revision = None
branch_labels = None
depends_on = None

def make_uuid():
    return str(uuid.uuid4())


def upgrade():
    op.create_table(
        'datapackage',
        sa.Column('id', sa.Unicode(), primary_key=True, default=make_uuid),
        sa.Column('package_id', sa.Unicode(), nullable=False),
        sa.Column('status', sa.Unicode(), default='created'),
        sa.Column('created', sa.DateTime(), default=dt.datetime.utcnow),
        sa.Column('data', JSON()),
        sa.Column('errors', JSON()),
    )
    op.create_table(
        'datapackage_resource',
        sa.Column('id', sa.Unicode(), primary_key=True, default=make_uuid),
        sa.Column('resource_id', sa.Unicode(), nullable=False),
        sa.Column('status', sa.Unicode(), default='created'),
        sa.Column('created', sa.DateTime(), default=dt.datetime.utcnow),
        sa.Column('data', JSON()),
        sa.Column('errors', JSON()),
    )

def downgrade():
    op.drop_table('datapackage')
    op.drop_table('datapackage_resource')
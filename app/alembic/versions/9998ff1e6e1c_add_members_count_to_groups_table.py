"""
add members count to groups table

Revision ID: 9998ff1e6e1c
Revises: 5eef6cabb65f
Create Date: 2024-12-04 23:50:43.432844

"""
from alembic import op
import sqlalchemy as sa


revision = '9998ff1e6e1c'
down_revision = '5eef6cabb65f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('groups', sa.Column('members_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('groups', 'members_count')

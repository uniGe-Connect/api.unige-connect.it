"""add_member_count

Revision ID: 85be5605114d
Revises: 71e472659dad
Create Date: 2024-12-04 14:33:00.461599

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '85be5605114d'
down_revision = '71e472659dad'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('groups', sa.Column('member_count', sa.Integer, default=1))

def downgrade():
    op.drop_column('groups', 'member_count')
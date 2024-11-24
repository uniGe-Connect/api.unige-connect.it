"""Add is_deleted column

Revision ID: 5155af76f1b9
Revises: f959a4378bb7
Create Date: 2024-11-22 11:29:24.765923

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5155af76f1b9'
down_revision = 'f959a4378bb7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "group",
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade():
    op.drop_column("group", "is_deleted")

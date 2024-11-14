"""setup_group

Revision ID: 71e472659dad
Revises: 88f05b3c9f29
Create Date: 2024-11-13 09:45:16.121208

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '71e472659dad'
down_revision = '88f05b3c9f29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("topic", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("type", sa.Enum('public_open', 'public_closed', 'private', name='group_types'), server_default='public_open', nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index('ix_group_owner_id', 'group', ['owner_id'])


def downgrade():
    op.drop_index(op.f("ix_group_owner_id"), table_name="group")
    op.drop_table("group")

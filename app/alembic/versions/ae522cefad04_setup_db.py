"""setup_db

Revision ID: ae522cefad04
Revises:
Create Date: 2024-11-12 21:56:55.912902

"""
from alembic import op
import sqlalchemy as sa

revision = 'ae522cefad04'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("surname", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), unique=True, nullable=False),
        sa.Column("type", sa.Enum('STUDENT', 'PROFESSOR', 'OPERATOR', 'ADMIN', name='user_roles'), server_default='STUDENT', nullable=False),
        
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("topic", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("type", sa.Enum('OPEN', 'CLOSED', 'PRIVATE', name='group_types'), server_default='OPEN', nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index('ix_group_owner_id', 'group', ['owner_id'])

def downgrade():
    op.drop_table("group")
    op.drop_index(op.f("ix_group_owner_id"), table_name="group")
    op.drop_table("user")


"""create_members_table

Revision ID: 5eef6cabb65f
Revises: 71e472659dad
Create Date: 2024-12-04 21:36:40.389144

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5eef6cabb65f'
down_revision = '85be5605114d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "members",
        sa.Column("id", sa.UUID, nullable=False),
        sa.Column("group_id", sa.UUID, nullable=False),
        sa.Column("user_id", sa.UUID, nullable=False),
        sa.Column(
            "role",
            sa.Enum('owner', 'member', name='member_types'),
            server_default='member', nullable=False
        ),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    
    op.create_index('ix_member_id', 'members', ['user_id'])
    op.create_index('ix_group_id', 'members', ['group_id'])
    op.create_index('ix_deleted_at', 'members', ['deleted_at'])
    
    pass


def downgrade():
    # Drop indices
    op.drop_index('ix_member_id', table_name='members')
    op.drop_index('ix_group_id', table_name='members')
    op.drop_index('ix_deleted_at', table_name='members')

    # Drop the table
    op.drop_table("members")

    # Drop the ENUM type
    op.execute("DROP TYPE IF EXISTS member_types")

from alembic import op
import sqlalchemy as sa

revision = '71e472659dad'
down_revision = '88f05b3c9f29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "groups",
        sa.Column("id", sa.UUID, nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("topic", sa.VARCHAR(), nullable=False),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        sa.Column(
            "type",
            sa.Enum('public_open', 'public_closed', 'private', name='group_types'),
            server_default='public_open', nullable=False
        ),

        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index('ix_group_owner_id', 'groups', ['owner_id'])


def downgrade():
    op.drop_index(op.f("ix_group_owner_id"), table_name="groups")
    op.drop_table("groups")

from alembic import op
import sqlalchemy as sa

revision = '88f05b3c9f29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False),
        sa.Column('serial_number', sa.String, nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("last_name", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), unique=True, nullable=False),
        sa.Column(
            "type",
            sa.Enum('student', 'professor', 'operator', 'admin', name='user_types'),
            server_default='student', nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),

        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")

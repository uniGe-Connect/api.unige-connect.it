"""create_courses_table

Revision ID: ea8ee73d5bbc
Revises: 5eef6cabb65f
Create Date: 2024-12-18 21:25:32.721820

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ea8ee73d5bbc'
down_revision = '5eef6cabb65f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "courses",
        sa.Column("id", sa.UUID, nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("courses")

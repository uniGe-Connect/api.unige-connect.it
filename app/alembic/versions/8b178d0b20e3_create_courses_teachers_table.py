"""create_courses_teachers_table

Revision ID: 8b178d0b20e3
Revises: ea8ee73d5bbc
Create Date: 2024-12-18 22:29:45.787056

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '8b178d0b20e3'
down_revision = 'ea8ee73d5bbc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "courses_teachers",
        sa.Column('course_id', sa.UUID, nullable=False),
        sa.Column('user_id', sa.UUID, nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
         sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("course_id", "user_id"),
    )
    op.create_index('ix_course_id', 'courses_teachers', ['course_id'])
    op.create_index('ix_user_id', 'courses_teachers', ['user_id'])


def downgrade():
    op.drop_table("courses_teachers")
    op.drop_index(op.f("ix_course_id"), table_name="courses_teachers")
    op.drop_index(op.f("ix_user_id"), table_name="courses_teachers")

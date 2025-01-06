"""add_id_to_courses__teachers_table

Revision ID: 76a089ef5368
Revises: e99ea3956bf3
Create Date: 2025-01-05 02:59:50.156122

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '76a089ef5368'
down_revision = 'e99ea3956bf3'
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing primary key
    op.drop_constraint('courses_teachers_pkey', 'courses_teachers', type_='primary')

    # Add new 'id' column as UUID primary key
    op.add_column(
        'courses_teachers',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False)
    ) 


def downgrade():
    # Remove the 'id' column
    op.drop_column('courses_teachers', 'id')

    # Reinstate original primary key
    op.create_primary_key('courses_teachers_pkey', 'courses_teachers', ['course_id', 'user_id'])

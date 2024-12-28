"""add course to groups table

Revision ID: e99ea3956bf3
Revises: 8b178d0b20e3
Create Date: 2024-12-28 12:03:10.054424

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e99ea3956bf3'
down_revision = '8b178d0b20e3'
branch_labels = None
depends_on = None


def upgrade():
    # remove the topic
    op.drop_column('groups', 'topic')
    # add the course column as a foreign key
    op.add_column('groups', sa.Column('course_id', sa.UUID(), nullable=False))
    op.create_foreign_key('fk_course_id', 'groups', 'courses', ['course_id'], ['id'])


def downgrade():
    # remove the course column
    op.drop_column('groups', 'course_id')
    # add the topic column
    op.add_column('groups', sa.Column('topic', sa.VARCHAR(), nullable=False))

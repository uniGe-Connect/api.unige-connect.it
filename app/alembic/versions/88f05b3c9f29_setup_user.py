"""setup_user

Revision ID: 88f05b3c9f29
Revises:
Create Date: 2024-11-13 09:45:12.630053

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '88f05b3c9f29'
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


def downgrade():
    op.drop_table('user')

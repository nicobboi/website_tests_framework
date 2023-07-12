"""Added report timestamps

Revision ID: 3ae0605c3d40
Revises: 374febea1217
Create Date: 2023-07-12 13:36:31.395982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ae0605c3d40'
down_revision = '374febea1217'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report', sa.Column('start_test_timestamp', sa.DateTime(timezone=True), nullable=False))
    op.add_column('report', sa.Column('end_test_timestamp', sa.DateTime(timezone=True), nullable=False))
    op.drop_column('report', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('report', sa.Column('timestamp', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column('report', 'end_test_timestamp')
    op.drop_column('report', 'start_test_timestamp')
    # ### end Alembic commands ###

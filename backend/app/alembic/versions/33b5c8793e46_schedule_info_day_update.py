"""Schedule info day update

Revision ID: 33b5c8793e46
Revises: a6e051d5db83
Create Date: 2023-08-11 10:13:44.830479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33b5c8793e46'
down_revision = 'a6e051d5db83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduleday',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('day', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scheduleday_id'), 'scheduleday', ['id'], unique=False)
    op.create_table('scheduleinfo_day',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('scheduleinfo_id', sa.UUID(), nullable=True),
    sa.Column('scheduleday_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['scheduleday_id'], ['scheduleday.id'], ),
    sa.ForeignKeyConstraint(['scheduleinfo_id'], ['scheduleinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scheduleinfo_day_id'), 'scheduleinfo_day', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scheduleinfo_day_id'), table_name='scheduleinfo_day')
    op.drop_table('scheduleinfo_day')
    op.drop_index(op.f('ix_scheduleday_id'), table_name='scheduleday')
    op.drop_table('scheduleday')
    # ### end Alembic commands ###

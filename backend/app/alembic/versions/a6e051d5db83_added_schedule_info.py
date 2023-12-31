"""Added schedule info

Revision ID: a6e051d5db83
Revises: 591706247f62
Create Date: 2023-08-11 09:40:29.209001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6e051d5db83'
down_revision = '591706247f62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduleinfo',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('min', sa.Integer(), nullable=True),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scheduleinfo_id'), 'scheduleinfo', ['id'], unique=False)
    op.add_column('schedule', sa.Column('scheduleinfo_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'schedule', 'scheduleinfo', ['scheduleinfo_id'], ['id'], ondelete='CASCADE')
    op.drop_column('schedule', 'day')
    op.drop_column('schedule', 'hour')
    op.drop_column('schedule', 'min')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('min', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('hour', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('schedule', sa.Column('day', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'scheduleinfo_id')
    op.drop_index(op.f('ix_scheduleinfo_id'), table_name='scheduleinfo')
    op.drop_table('scheduleinfo')
    # ### end Alembic commands ###

"""schedule update

Revision ID: 591706247f62
Revises: b7acf845ed4d
Create Date: 2023-08-08 15:16:30.289269

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '591706247f62'
down_revision = 'b7acf845ed4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_crontab_id'), table_name='crontab')
    op.drop_table('crontab')
    op.create_table('schedule',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('type_id', sa.UUID(), nullable=False),
    sa.Column('website_id', sa.UUID(), nullable=False),
    sa.Column('min', sa.Integer(), nullable=True),
    sa.Column('hour', sa.Integer(), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('n_run', sa.Integer(), nullable=False),
    sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_time_launched', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['website_id'], ['website.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_id'), 'schedule', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_score_id'), table_name='score')
    op.drop_table('score')
    op.drop_index(op.f('ix_report_id'), table_name='report')
    op.drop_table('report')
    op.drop_index(op.f('ix_tool_id'), table_name='tool')
    op.drop_table('tool')
    op.drop_index(op.f('ix_token_token'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_schedule_id'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_index(op.f('ix_website_id'), table_name='website')
    op.drop_table('website')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_type_id'), table_name='type')
    op.drop_table('type')
    # ### end Alembic commands ###

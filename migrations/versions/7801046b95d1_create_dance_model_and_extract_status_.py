"""Create Dance model and extract status from Song to Dance

Revision ID: 7801046b95d1
Revises: 3bef545e708e
Create Date: 2026-01-22 15:30:51.449976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7801046b95d1'
down_revision = '3bef545e708e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('dances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['song_id'], ['songs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_column('status')


def downgrade():
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=50), autoincrement=False, nullable=False, default='to do'))

    op.drop_table('dances')

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

    # Migrate existing status data from songs to dances
    connection = op.get_bind()
    songs_table = sa.table(
        'songs',
        sa.column('id', sa.Integer),
        sa.column('status', sa.VARCHAR(length=50)),
    )
    dances_table = sa.table(
        'dances',
        sa.column('id', sa.Integer),
        sa.column('song_id', sa.Integer),
        sa.column('status', sa.VARCHAR(length=50)),
    )

    # Set dances.status based on the corresponding songs.status entry.
    song_status_subquery = (
        sa.select(songs_table.c.id, songs_table.c.status)
    )
    results = connection.execute(song_status_subquery).fetchall()
    for song_id, status in results:
        connection.execute(
            dances_table.insert().values(song_id=song_id, status=status)
        )

    # Drop the status column from songs table
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.drop_column('status')


def downgrade():
    # Re-add the status column as nullable first so existing rows are allowed.
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('status', sa.VARCHAR(length=50), autoincrement=False, nullable=True)
        )

    # Backfill songs.status from dances.status where possible.
    connection = op.get_bind()
    songs_table = sa.table(
        'songs',
        sa.column('id', sa.Integer),
        sa.column('status', sa.VARCHAR(length=50)),
    )
    dances_table = sa.table(
        'dances',
        sa.column('song_id', sa.Integer),
        sa.column('status', sa.VARCHAR(length=50)),
    )

    # Set songs.status based on the corresponding dances.status entry.
    status_subquery = (
        sa.select(dances_table.c.status)
        .where(dances_table.c.song_id == songs_table.c.id)
        .correlate(songs_table)
        .scalar_subquery()
    )
    connection.execute(
        songs_table.update().values(status=status_subquery)
    )

    # For any songs without a dance entry, default status back to 'to do'.
    connection.execute(
        songs_table.update()
        .where(songs_table.c.status.is_(None))
        .values(status='to do')
    )

    # Now enforce NOT NULL on the status column.
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.alter_column(
            'status',
            existing_type=sa.VARCHAR(length=50),
            nullable=False,
        )
    op.drop_table('dances')

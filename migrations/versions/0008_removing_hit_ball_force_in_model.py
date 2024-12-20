"""Removing hit_ball.force in  model

Revision ID: 0008
Revises: 0006
Create Date: 2024-09-01 10:31:55.814440

"""

from migrations.versions import log
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        log.info(f"{revision} - Creating table 'ball_potted_event_data'...")
        op.create_table(
            "ball_potted_event_data",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("event_id", sa.Integer(), nullable=False),
            sa.Column("ball_number", sa.Integer(), nullable=False),
            sa.Column("pocket_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
    except Exception as e:
        log.error(
            f"{revision} - Error creating table 'ball_potted_event_data'. message: {e}"
        )
    try:
        log.info(f"{revision} - Creating table 'foul_event_data'...")
        op.create_table(
            "foul_event_data",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("event_id", sa.Integer(), nullable=False),
            sa.Column("reason", sa.String(length=255), nullable=False),
            sa.ForeignKeyConstraint(
                ["event_id"],
                ["events.id"],
                ondelete="CASCADE",
                name="fk_ball_potted_event_events",
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except Exception as e:
        log.error(f"{revision} - Error creating table 'foul_event_data'. message: {e}")
    try:
        log.info(f"{revision} - Creating table 'hit_ball_event_data'...")
        op.create_table(
            "hit_ball_event_data",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("event_id", sa.Integer(), nullable=False),
            sa.Column("ball_number", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["event_id"],
                ["events.id"],
                ondelete="CASCADE",
                name="kf_hit_ball_event_events",
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except Exception as e:
        log.error(
            f"{revision} - Error creating table 'hit_ball_event_data'. message: {e}"
        )
    try:
        with op.batch_alter_table("events", schema=None) as batch_op:
            batch_op.alter_column(
                "match_id", existing_type=sa.INTEGER(), nullable=False
            )
            batch_op.alter_column(
                "event_type", existing_type=sa.VARCHAR(length=11), nullable=False
            )
            batch_op.alter_column(
                "description",
                existing_type=sa.VARCHAR(),
                type_=sa.Text(),
                existing_nullable=True,
            )
            batch_op.drop_constraint("fk_games_id_events", type_="foreignkey")
            batch_op.drop_constraint("fk_matches_id_events", type_="foreignkey")
            batch_op.create_foreign_key(
                "fk_matches_match_id",
                "matches",
                ["match_id"],
                ["id"],
                ondelete="CASCADE",
            )
            batch_op.drop_column("ball_number")
            batch_op.drop_column("success")
            batch_op.drop_column("game_id")
    except Exception as e:
        log.error(f"{revision} - Error altering table 'events'. message: {e}")
    with op.batch_alter_table("games", schema=None) as batch_op:
        batch_op.add_column(sa.Column("player1_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("player2_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_player1_players_id", "players", ["player1_id"], ["id"]
        )
        batch_op.create_foreign_key(
            "fk_player2_players_id", "players", ["player2_id"], ["id"]
        )

    with op.batch_alter_table("matches", schema=None) as batch_op:
        batch_op.add_column(sa.Column("game_type", sa.String(), nullable=True))

    with op.batch_alter_table("players", schema=None) as batch_op:
        batch_op.add_column(sa.Column("wins", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("losses", sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("players", schema=None) as batch_op:
        batch_op.drop_column("losses")
        batch_op.drop_column("wins")

    with op.batch_alter_table("matches", schema=None) as batch_op:
        batch_op.drop_column("game_type")

    with op.batch_alter_table("games", schema=None) as batch_op:
        batch_op.drop_constraint("fk_player1_players_id", type_="foreignkey")
        batch_op.drop_constraint("fk_player2_players_id", type_="foreignkey")
        batch_op.drop_column("player2_id")
        batch_op.drop_column("player1_id")

    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.add_column(sa.Column("game_id", sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column("success", sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column("ball_number", sa.INTEGER(), nullable=True))
        batch_op.drop_constraint("fk_matches_match_id", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_matches_id_events", "matches", ["match_id"], ["id"]
        )
        batch_op.create_foreign_key("fk_games_id_events", "games", ["game_id"], ["id"])
        batch_op.alter_column(
            "description",
            existing_type=sa.Text(),
            type_=sa.VARCHAR(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "event_type", existing_type=sa.VARCHAR(length=11), nullable=True
        )
        batch_op.alter_column("match_id", existing_type=sa.INTEGER(), nullable=True)

    op.drop_table("hit_ball_event_data")
    op.drop_table("foul_event_data")
    op.drop_table("ball_potted_event_data")
    # ### end Alembic commands ###

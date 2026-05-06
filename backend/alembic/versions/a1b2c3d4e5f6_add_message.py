"""add message

Revision ID: a1b2c3d4e5f6
Revises: f273b29c941a
Create Date: 2026-05-06 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel

from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: str | None = "f273b29c941a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("sender_address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["room.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_room_id"), "message", ["room_id"], unique=False)
    op.create_index(
        op.f("ix_message_sender_address"),
        "message",
        ["sender_address"],
        unique=False,
    )
    op.create_index(
        op.f("ix_message_created_at"), "message", ["created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_message_created_at"), table_name="message")
    op.drop_index(op.f("ix_message_sender_address"), table_name="message")
    op.drop_index(op.f("ix_message_room_id"), table_name="message")
    op.drop_table("message")

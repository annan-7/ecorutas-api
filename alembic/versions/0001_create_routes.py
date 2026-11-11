"""create routes table"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "routes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("interesting_fact", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(2048), nullable=False),
        sa.Column("location", sa.String(120), nullable=False),
        sa.Column("distance_km", sa.Float(), nullable=False),
        sa.Column("difficulty", sa.String(20), nullable=False),
        sa.Column("route_type", sa.String(30), nullable=False),
        sa.Column("duration_hours", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("altitude_meters", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    for column in ("name", "location", "difficulty", "is_active"):
        op.create_index(f"ix_routes_{column}", "routes", [column])


def downgrade() -> None:
    op.drop_table("routes")

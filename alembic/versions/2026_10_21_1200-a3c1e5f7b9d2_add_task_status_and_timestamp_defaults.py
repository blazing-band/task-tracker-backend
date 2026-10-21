"""add task status and timestamp defaults

Revision ID: a3c1e5f7b9d2
Revises: 6f26bbd64e34
Create Date: 2026-10-21 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3c1e5f7b9d2"
down_revision: str | Sequence[str] | None = "6f26bbd64e34"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("task", "status", server_default="IN_PROGRESS")
    op.alter_column("task", "timestamp", server_default=sa.func.now())


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("task", "timestamp", server_default=None)
    op.alter_column("task", "status", server_default=None)

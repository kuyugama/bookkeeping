"""Initial

Revision ID: 9111d65435ba
Revises: 
Create Date: 2025-01-17 13:19:25.521972

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9111d65435ba"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "service_accounts",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("normal", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=255), nullable=False),
        sa.Column("balance", sa.Numeric(precision=28, scale=8), nullable=False),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("normal IN (1, -1)", name="check_normal_positive_or_negative"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_accounts_balance"), "service_accounts", ["balance"], unique=False
    )
    op.create_index(
        op.f("ix_service_accounts_created_at"), "service_accounts", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_service_accounts_currency"), "service_accounts", ["currency"], unique=False
    )
    op.create_index(op.f("ix_service_accounts_id"), "service_accounts", ["id"], unique=False)
    op.create_index(op.f("ix_service_accounts_name"), "service_accounts", ["name"], unique=True)
    op.create_index(
        op.f("ix_service_accounts_updated_at"), "service_accounts", ["updated_at"], unique=False
    )
    op.create_table(
        "service_transactions",
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_transactions_category"), "service_transactions", ["category"], unique=False
    )
    op.create_index(
        op.f("ix_service_transactions_created_at"),
        "service_transactions",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_service_transactions_currency"), "service_transactions", ["currency"], unique=False
    )
    op.create_index(
        op.f("ix_service_transactions_id"), "service_transactions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_service_transactions_updated_at"),
        "service_transactions",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "service_transfers",
        sa.Column("amount", sa.Numeric(precision=28, scale=8), nullable=False),
        sa.Column("account_id", sa.BIGINT(), nullable=True),
        sa.Column("transaction_id", sa.BIGINT(), nullable=True),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["service_accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["transaction_id"], ["service_transactions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_transfers_created_at"), "service_transfers", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_service_transfers_id"), "service_transfers", ["id"], unique=False)
    op.create_index(
        op.f("ix_service_transfers_updated_at"), "service_transfers", ["updated_at"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_service_transfers_updated_at"), table_name="service_transfers")
    op.drop_index(op.f("ix_service_transfers_id"), table_name="service_transfers")
    op.drop_index(op.f("ix_service_transfers_created_at"), table_name="service_transfers")
    op.drop_table("service_transfers")
    op.drop_index(op.f("ix_service_transactions_updated_at"), table_name="service_transactions")
    op.drop_index(op.f("ix_service_transactions_id"), table_name="service_transactions")
    op.drop_index(op.f("ix_service_transactions_currency"), table_name="service_transactions")
    op.drop_index(op.f("ix_service_transactions_created_at"), table_name="service_transactions")
    op.drop_index(op.f("ix_service_transactions_category"), table_name="service_transactions")
    op.drop_table("service_transactions")
    op.drop_index(op.f("ix_service_accounts_updated_at"), table_name="service_accounts")
    op.drop_index(op.f("ix_service_accounts_name"), table_name="service_accounts")
    op.drop_index(op.f("ix_service_accounts_id"), table_name="service_accounts")
    op.drop_index(op.f("ix_service_accounts_currency"), table_name="service_accounts")
    op.drop_index(op.f("ix_service_accounts_created_at"), table_name="service_accounts")
    op.drop_index(op.f("ix_service_accounts_balance"), table_name="service_accounts")
    op.drop_table("service_accounts")
    # ### end Alembic commands ###

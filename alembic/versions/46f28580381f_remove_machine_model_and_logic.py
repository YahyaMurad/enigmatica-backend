"""Remove machine model and logic

Revision ID: 46f28580381f
Revises: ef551f7e997e
Create Date: 2025-11-03 23:01:07.454630
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46f28580381f'
down_revision: Union[str, Sequence[str], None] = 'ef551f7e997e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the FK constraint first
    op.drop_constraint(op.f('heartbeats_machine_id_fkey'), 'heartbeats', type_='foreignkey')

    # Drop the column that used the FK
    op.drop_column('heartbeats', 'machine_id')

    # Now it's safe to drop the machines table
    op.drop_index(op.f('ix_machines_id'), table_name='machines')
    op.drop_table('machines')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate machines table
    op.create_table(
        'machines',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('machine_name', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('machines_user_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('machines_pkey'))
    )
    op.create_index(op.f('ix_machines_id'), 'machines', ['id'], unique=False)

    # Re-add column and foreign key in heartbeats
    op.add_column('heartbeats', sa.Column('machine_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f('heartbeats_machine_id_fkey'),
        'heartbeats',
        'machines',
        ['machine_id'],
        ['id']
    )

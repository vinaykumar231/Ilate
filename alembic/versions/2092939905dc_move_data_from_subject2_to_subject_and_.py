"""Move data from subject2 to subject and drop subject2

Revision ID: 2092939905dc
Revises: 231846bff22f
Create Date: 2024-05-24 15:49:34.291546

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2092939905dc'
down_revision: Union[str, None] = '231846bff22f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Move data from subject2 to subject if necessary
    op.execute("""
        UPDATE mails
        SET subject = subject2
        WHERE subject2 IS NOT NULL AND subject IS NULL
    """)

    # Step 2: Drop any constraints on the subject2 column if necessary
    with op.batch_alter_table('mails') as batch_op:
        # Example: Drop an index or constraint (modify based on actual constraints)
        batch_op.drop_constraint('uq_mails_subject2', type_='unique', if_exists=True)
        batch_op.drop_index('ix_mails_subject2', if_exists=True)

    # Step 3: Drop the subject2 column
    op.drop_column('mails', 'subject2')


def downgrade() -> None:
    # Step 1: Add the subject2 column back
    op.add_column('mails', sa.Column('subject2', sa.String(length=255), nullable=True))

    # Step 2: Optionally move data back from subject to subject2
    op.execute("""
        UPDATE mails
        SET subject2 = subject
        WHERE subject IS NOT NULL AND subject2 IS NULL
    """)

    # Step 3: Re-add any constraints on the subject2 column if necessary
    with op.batch_alter_table('mails') as batch_op:
        # Example: Recreate an index or constraint (modify based on actual constraints)
        batch_op.create_unique_constraint('uq_mails_subject2', ['subject2'])
        batch_op.create_index('ix_mails_subject2', ['subject2'])

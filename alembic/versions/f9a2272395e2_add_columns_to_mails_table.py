"""description of migration

Revision ID: 231846bff22f
Revises: 
Create Date: 2024-05-24 14:47:20.078091

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '231846bff22f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the email column
    op.add_column('mails', sa.Column('email', sa.String(length=255), nullable=True))
    
    # Add the message column
    op.add_column('mails', sa.Column('message', sa.String(length=255), nullable=True))
    
    # Add the name column
    op.add_column('mails', sa.Column('name', sa.String(length=255), nullable=True))
    
    # Add the phone column
    op.add_column('mails', sa.Column('phone', sa.String(length=20), nullable=True))
    
    # Add the subject column
    op.add_column('mails', sa.Column('subject', sa.String(length=255), nullable=True))
    


def downgrade() -> None:
    # Drop all added columns
    op.drop_column('mails', 'email')
    op.drop_column('mails', 'message')
    op.drop_column('mails', 'name')
    op.drop_column('mails', 'phone')
    op.drop_column('mails', 'subject')

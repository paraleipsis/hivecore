"""update

Revision ID: bbe483893d49
Revises: 44861d2a9c87
Create Date: 2023-05-13 21:14:48.529939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbe483893d49'
down_revision = '44861d2a9c87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nodes', sa.Column('token', sa.String(), nullable=False))
    op.create_index(op.f('ix_nodes_token'), 'nodes', ['token'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_nodes_token'), table_name='nodes')
    op.drop_column('nodes', 'token')
    # ### end Alembic commands ###

"""database update

Revision ID: 3b85552efc8d
Revises: 227f971c07bf
Create Date: 2023-03-12 20:24:53.712307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b85552efc8d'
down_revision = '227f971c07bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('nodes', 'environment_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index('ix_nodes_name', table_name='nodes')
    op.create_index(op.f('ix_nodes_name'), 'nodes', ['name'], unique=False)
    op.create_unique_constraint(None, 'nodes', ['environment_id', 'name'])
    op.drop_constraint('nodes_environment_id_fkey', 'nodes', type_='foreignkey')
    op.create_foreign_key(None, 'nodes', 'environments', ['environment_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nodes', type_='foreignkey')
    op.create_foreign_key('nodes_environment_id_fkey', 'nodes', 'environments', ['environment_id'], ['id'])
    op.drop_constraint(None, 'nodes', type_='unique')
    op.drop_index(op.f('ix_nodes_name'), table_name='nodes')
    op.create_index('ix_nodes_name', 'nodes', ['name'], unique=False)
    op.alter_column('nodes', 'environment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###

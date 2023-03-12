"""database update

Revision ID: 79d66f794c0d
Revises: 2812169783fb
Create Date: 2023-03-12 17:35:05.825619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d66f794c0d'
down_revision = '2812169783fb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_environments_name', table_name='environments')
    op.create_index(op.f('ix_environments_name'), 'environments', ['name'], unique=False)
    op.drop_constraint('environments_platform_id_fkey', 'environments', type_='foreignkey')
    op.create_foreign_key(None, 'environments', 'platforms', ['platform_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'environments', type_='foreignkey')
    op.create_foreign_key('environments_platform_id_fkey', 'environments', 'platforms', ['platform_id'], ['id'])
    op.drop_index(op.f('ix_environments_name'), table_name='environments')
    op.create_index('ix_environments_name', 'environments', ['name'], unique=False)
    # ### end Alembic commands ###

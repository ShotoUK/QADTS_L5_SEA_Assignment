"""Migration 2

Revision ID: 67bcfd2e921d
Revises: 918e531e9887
Create Date: 2024-02-28 15:52:43.450978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bcfd2e921d'
down_revision = '918e531e9887'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('Role',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('Role',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###

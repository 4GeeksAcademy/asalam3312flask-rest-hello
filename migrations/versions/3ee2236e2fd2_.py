"""empty message

Revision ID: 3ee2236e2fd2
Revises: 3c7d0165c0c1
Create Date: 2024-04-28 01:23:01.306096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ee2236e2fd2'
down_revision = '3c7d0165c0c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorites', ['favorites_id'], ['id'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorites', ['favorites_id'], ['id'])

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'favorites', ['favorites_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorites_id')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorites_id')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('favorites_id')

    op.drop_table('favorites')
    # ### end Alembic commands ###

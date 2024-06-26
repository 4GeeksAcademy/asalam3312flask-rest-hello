"""empty message

Revision ID: 3c7d0165c0c1
Revises: a5cffa318ac2
Create Date: 2024-04-25 02:52:56.389588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c7d0165c0c1'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('hair_color', sa.String(length=40), nullable=False),
    sa.Column('eye_color', sa.String(length=40), nullable=False),
    sa.Column('skin_color', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('gravity', sa.String(length=80), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=80), nullable=True),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('model', sa.String(length=80), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('cost_in_credits', sa.String(length=80), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.Boolean(create_constraint=50), nullable=False))
        batch_op.add_column(sa.Column('name', sa.Boolean(create_constraint=50), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.Boolean(create_constraint=50), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('last_name')
        batch_op.drop_column('name')
        batch_op.drop_column('username')

    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###

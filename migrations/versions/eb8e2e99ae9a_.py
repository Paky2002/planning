"""empty message

Revision ID: eb8e2e99ae9a
Revises: 
Create Date: 2021-07-06 15:59:48.217620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb8e2e99ae9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('preventivi')
    op.drop_table('preventivo')
    op.drop_table('students')
    op.drop_table('ciao')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ciao',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cioao', sa.VARCHAR(length=100), nullable=True),
    sa.Column('aiaoao', sa.DATE(), nullable=True),
    sa.Column('bvhg', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('city', sa.VARCHAR(length=50), nullable=True),
    sa.Column('addr', sa.VARCHAR(length=200), nullable=True),
    sa.Column('pin', sa.VARCHAR(length=10), nullable=True),
    sa.PrimaryKeyConstraint('student_id')
    )
    op.create_table('preventivo',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cognome', sa.VARCHAR(length=100), nullable=True),
    sa.Column('check_in', sa.DATE(), nullable=True),
    sa.Column('check_out', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('preventivi',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cognome', sa.VARCHAR(length=100), nullable=True),
    sa.Column('check_in', sa.DATE(), nullable=True),
    sa.Column('check_out', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
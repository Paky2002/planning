"""empty message

Revision ID: 0fdbedf76985
Revises: 58d04e0ab4a2
Create Date: 2021-08-27 10:16:56.675144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fdbedf76985'
down_revision = '58d04e0ab4a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contatti', sa.Column('paeseNascita', sa.String(length=100), nullable=True))
    op.add_column('contatti', sa.Column('paeseResidenza', sa.String(length=100), nullable=True))
    op.add_column('contatti', sa.Column('comuneNascita', sa.String(length=100), nullable=True))
    op.add_column('contatti', sa.Column('comuneResidenza', sa.String(length=100), nullable=True))
    op.drop_column('contatti', 'comune')
    op.drop_column('contatti', 'paese')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contatti', sa.Column('paese', sa.VARCHAR(length=100), nullable=True))
    op.add_column('contatti', sa.Column('comune', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('contatti', 'comuneResidenza')
    op.drop_column('contatti', 'comuneNascita')
    op.drop_column('contatti', 'paeseResidenza')
    op.drop_column('contatti', 'paeseNascita')
    # ### end Alembic commands ###

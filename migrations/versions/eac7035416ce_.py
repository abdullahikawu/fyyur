"""empty message

Revision ID: eac7035416ce
Revises: 974c48e67ff8
Create Date: 2022-06-04 22:52:05.956614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eac7035416ce'
down_revision = '974c48e67ff8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.String(length=500), nullable=True))
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_talent', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###

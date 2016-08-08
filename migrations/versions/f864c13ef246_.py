"""empty message

Revision ID: f864c13ef246
Revises: b66a62de934a
Create Date: 2016-08-07 21:25:38.389838

"""

# revision identifiers, used by Alembic.
revision = 'f864c13ef246'
down_revision = 'b66a62de934a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('timestamp', sa.String(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'timestamp')
    ### end Alembic commands ###

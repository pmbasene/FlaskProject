"""update

Revision ID: 0f80e7269c49
Revises: 5282ceac1308
Create Date: 2020-05-22 00:10:39.817199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f80e7269c49'
down_revision = '5282ceac1308'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather', sa.Column('date_posted', sa.DateTime(), nullable=True))
    op.add_column('weather', sa.Column('image_file', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weather', 'image_file')
    op.drop_column('weather', 'date_posted')
    # ### end Alembic commands ###
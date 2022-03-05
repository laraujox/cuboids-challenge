"""empty message

Revision ID: 8b40144a3f48
Revises: 833724243ce0
Create Date: 2022-03-05 17:45:16.511527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b40144a3f48'
down_revision = '833724243ce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bags', sa.Column('title', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bags', 'title')
    # ### end Alembic commands ###

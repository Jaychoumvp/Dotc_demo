"""empty message

Revision ID: 142b7e2b2cd3
Revises: 9525b9b3a0cd
Create Date: 2020-10-24 23:28:26.686016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '142b7e2b2cd3'
down_revision = '9525b9b3a0cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_article_basic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=130), nullable=True),
    sa.Column('cover', sa.JSON(), nullable=True),
    sa.Column('ctime', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_article_content',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('article_id')
    )
    op.create_table('news_attitude',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('attitude', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_channel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_user_channel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('sequence', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_user_channel')
    op.drop_table('news_collection')
    op.drop_table('news_channel')
    op.drop_table('news_attitude')
    op.drop_table('news_article_content')
    op.drop_table('news_article_basic')
    # ### end Alembic commands ###

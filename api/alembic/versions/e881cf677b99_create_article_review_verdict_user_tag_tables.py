"""create article review verdict user tag tables

Revision ID: e881cf677b99
Revises: 0480e04f2307
Create Date: 2020-04-03 14:07:42.833977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e881cf677b99'
down_revision = '0480e04f2307'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tag',
        sa.Column('id',
            sa.BigInteger(),
            autoincrement=True,
            primary_key=True
        ),
        sa.Column('text',
            sa.Text(),
            unique=True
        ))

    op.create_table('article_tag',
        sa.Column('id',
            sa.BigInteger(),
            autoincrement=True,
            primary_key=True
        ),
        sa.Column('articleId',
                  sa.BigInteger(),
                  sa.ForeignKey('article.id'),
                  primary_key=True),
        sa.Column('tagId',
                  sa.BigInteger(),
                  sa.ForeignKey('tag.id'),
                  primary_key=True))

    op.create_table('review_tag',
        sa.Column('id',
            sa.BigInteger(),
            autoincrement=True,
            primary_key=True
        ),
        sa.Column('reviewId',
                  sa.BigInteger(),
                  sa.ForeignKey('review.id'),
                  primary_key=True),
        sa.Column('tagId',
                  sa.BigInteger(),
                  sa.ForeignKey('tag.id'),
                  primary_key=True))

    op.create_table('verdict_tag',
        sa.Column('id',
            sa.BigInteger(),
            autoincrement=True,
            primary_key=True
        ),
        sa.Column('verdictId',
                  sa.BigInteger(),
                  sa.ForeignKey('verdict.id'),
                  primary_key=True),
        sa.Column('tagId',
                  sa.BigInteger(),
                  sa.ForeignKey('tag.id'),
                  primary_key=True))

    op.create_table('user_tag',
        sa.Column('id',
            sa.BigInteger(),
            autoincrement=True,
            primary_key=True
        ),
        sa.Column('userId',
                  sa.BigInteger(),
                  sa.ForeignKey('user.id'),
                  primary_key=True),
        sa.Column('tagId',
                  sa.BigInteger(),
                  sa.ForeignKey('tag.id'),
                  primary_key=True))


def downgrade():
    op.drop_table('article_tag')
    op.drop_table('review_tag')
    op.drop_table('verdict_tag')
    op.drop_table('user_tag')
    op.drop_table('tag')

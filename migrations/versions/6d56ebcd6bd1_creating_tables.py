"""creating tables

Revision ID: 6d56ebcd6bd1
Revises: 
Create Date: 2021-07-21 10:23:06.865460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d56ebcd6bd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('user_email', sa.String(length=60), nullable=True),
    sa.Column('user_password', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_user_password'), 'user', ['user_password'], unique=False)
    op.create_table('course',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(length=100), nullable=True),
    sa.Column('course_instructor', sa.String(length=50), nullable=False),
    sa.Column('course_fee', sa.Integer(), nullable=True),
    sa.Column('course_created', sa.DateTime(), nullable=False),
    sa.Column('course_duration', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_instructor'], ['user.id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('course')
    op.drop_index(op.f('ix_user_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###

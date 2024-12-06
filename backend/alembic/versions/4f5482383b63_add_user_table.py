"""Add User table

Revision ID: 4f5482383b63
Revises: 5ea9047c43e3
Create Date: 2024-12-06 15:49:34.346390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f5482383b63'
down_revision: Union[str, None] = '5ea9047c43e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('conversationID', sa.String(length=255), nullable=True),
    sa.Column('timeStamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('query', sa.String(length=255), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('userId', sa.String(length=255), nullable=True),
    sa.Column('knowledgeBaseId', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('conversationsList',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lastChatTime', sa.TIMESTAMP(), nullable=False),
    sa.Column('conversationName', sa.String(length=255), nullable=True),
    sa.Column('num_conversation', sa.Integer(), nullable=True),
    sa.Column('knowledgeBaseId', sa.String(length=255), nullable=True),
    sa.Column('userId', sa.String(length=255), nullable=True),
    sa.Column('delete_sign', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('docIndexStatus',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('index_status', sa.Integer(), nullable=True),
    sa.Column('knowledgeBaseId', sa.String(length=255), nullable=True),
    sa.Column('doc_id', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('docsInfo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('doc_name', sa.String(length=255), nullable=True),
    sa.Column('knowledgeBaseId', sa.String(length=255), nullable=True),
    sa.Column('retriever_num', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('doc_type', sa.String(length=255), nullable=True),
    sa.Column('doc_size', sa.Integer(), nullable=True),
    sa.Column('save_id', sa.String(length=255), nullable=True),
    sa.Column('delete_sign', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('knowledgeBasesList',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('knowledgeBaseNameId', sa.String(length=18), nullable=True),
    sa.Column('knowledgeBaseName', sa.String(length=255), nullable=True),
    sa.Column('docs_num', sa.Integer(), nullable=True),
    sa.Column('words_num', sa.Integer(), nullable=True),
    sa.Column('related_conversations', sa.Integer(), nullable=True),
    sa.Column('delete_sign', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_by', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userInfo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.String(length=18), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('create_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('delete_sign', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userInfo_email'), 'userInfo', ['email'], unique=True)
    op.create_index(op.f('ix_userInfo_userId'), 'userInfo', ['userId'], unique=True)
    op.create_index(op.f('ix_userInfo_username'), 'userInfo', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userInfo_username'), table_name='userInfo')
    op.drop_index(op.f('ix_userInfo_userId'), table_name='userInfo')
    op.drop_index(op.f('ix_userInfo_email'), table_name='userInfo')
    op.drop_table('userInfo')
    op.drop_table('knowledgeBasesList')
    op.drop_table('docsInfo')
    op.drop_table('docIndexStatus')
    op.drop_table('conversationsList')
    op.drop_table('chat_messages')
    # ### end Alembic commands ###

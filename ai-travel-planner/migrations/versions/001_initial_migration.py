"""Initial migration with core models

Revision ID: 001
Revises: 
Create Date: 2025-01-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE travelstyle AS ENUM ('family', 'couple', 'business', 'solo', 'group', 'adventure', 'luxury', 'budget')")
    op.execute("CREATE TYPE planstatus AS ENUM ('planning', 'confirmed', 'completed', 'cancelled')")
    op.execute("CREATE TYPE conversationstatus AS ENUM ('active', 'paused', 'completed', 'archived')")
    op.execute("CREATE TYPE messagerole AS ENUM ('user', 'assistant', 'system')")
    op.execute("CREATE TYPE currency AS ENUM ('USD', 'EUR', 'CNY', 'JPY', 'GBP')")
    
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=False, default={}),
        sa.Column('travel_history', sa.JSON(), nullable=False, default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email')),
        sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    
    # Create travel_plans table
    op.create_table('travel_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('destination', sa.String(length=100), nullable=False),
        sa.Column('destinations', sa.JSON(), nullable=False, default=[]),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('budget', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('currency', postgresql.ENUM('USD', 'EUR', 'CNY', 'JPY', 'GBP', name='currency'), nullable=False, default='USD'),
        sa.Column('estimated_total_cost', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('status', postgresql.ENUM('planning', 'confirmed', 'completed', 'cancelled', name='planstatus'), nullable=False, default='planning'),
        sa.Column('travelers_count', sa.Integer(), nullable=False, default=1),
        sa.Column('travel_style', sa.String(length=50), nullable=False),
        sa.Column('flights', sa.JSON(), nullable=False, default=[]),
        sa.Column('hotels', sa.JSON(), nullable=False, default=[]),
        sa.Column('itinerary', sa.JSON(), nullable=False, default=[]),
        sa.Column('special_requirements', sa.JSON(), nullable=False, default=[]),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_travel_plans_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_travel_plans'))
    )
    op.create_index(op.f('ix_travel_plans_destination'), 'travel_plans', ['destination'], unique=False)
    op.create_index(op.f('ix_travel_plans_start_date'), 'travel_plans', ['start_date'], unique=False)
    op.create_index(op.f('ix_travel_plans_end_date'), 'travel_plans', ['end_date'], unique=False)
    op.create_index('ix_travel_plans_user_status', 'travel_plans', ['user_id', 'status'], unique=False)
    op.create_index('ix_travel_plans_dates', 'travel_plans', ['start_date', 'end_date'], unique=False)
    
    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('status', postgresql.ENUM('active', 'paused', 'completed', 'archived', name='conversationstatus'), nullable=False, default='active'),
        sa.Column('context', sa.JSON(), nullable=False, default={}),
        sa.Column('total_tokens', sa.Integer(), nullable=False, default=0),
        sa.Column('total_cost', sa.Float(), nullable=False, default=0.0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_conversations_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_conversations'))
    )
    op.create_index('ix_conversations_user_status', 'conversations', ['user_id', 'status'], unique=False)
    op.create_index('ix_conversations_updated', 'conversations', ['updated_at'], unique=False)
    
    # Create messages table
    op.create_table('messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', postgresql.ENUM('user', 'assistant', 'system', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=False, default={}),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('model_name', sa.String(length=100), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name=op.f('fk_messages_conversation_id_conversations')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    op.create_index('ix_messages_conversation_timestamp', 'messages', ['conversation_id', 'timestamp'], unique=False)
    op.create_index('ix_messages_role', 'messages', ['role'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('travel_plans')
    op.drop_table('users')
    
    # Drop enum types
    op.execute("DROP TYPE IF EXISTS messagerole")
    op.execute("DROP TYPE IF EXISTS conversationstatus")
    op.execute("DROP TYPE IF EXISTS planstatus")
    op.execute("DROP TYPE IF EXISTS currency")
    op.execute("DROP TYPE IF EXISTS travelstyle")
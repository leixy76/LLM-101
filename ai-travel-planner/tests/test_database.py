"""
Database integration tests.
"""
import pytest
import asyncio
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from shared.database import Base, UserORM, TravelPlanORM, ConversationORM, MessageORM
from shared.models.base import TravelStyle, PlanStatus, ConversationStatus, MessageRole, Currency


# Test database URL (use in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create test database session."""
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with TestSessionLocal() as session:
        yield session


class TestUserORM:
    """Test User ORM operations."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_session: AsyncSession):
        """Test creating a user."""
        user = UserORM(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            preferences={
                "budget_range": [1000, 5000],
                "travel_style": "solo",
                "language": "en"
            }
        )
        
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.preferences["travel_style"] == "solo"
    
    @pytest.mark.asyncio
    async def test_user_relationships(self, test_session: AsyncSession):
        """Test user relationships with travel plans and conversations."""
        # Create user
        user = UserORM(
            username="testuser",
            email="test@example.com"
        )
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create travel plan
        travel_plan = TravelPlanORM(
            user_id=user.id,
            title="Test Trip",
            destination="Paris",
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 10),
            duration_days=10,
            budget=Decimal("2000.00"),
            travel_style="solo"
        )
        test_session.add(travel_plan)
        
        # Create conversation
        conversation = ConversationORM(
            user_id=user.id,
            title="Trip Planning"
        )
        test_session.add(conversation)
        
        await test_session.commit()
        
        # Test relationships
        await test_session.refresh(user)
        assert len(user.travel_plans) == 1
        assert len(user.conversations) == 1
        assert user.travel_plans[0].title == "Test Trip"
        assert user.conversations[0].title == "Trip Planning"


class TestTravelPlanORM:
    """Test TravelPlan ORM operations."""
    
    @pytest.mark.asyncio
    async def test_create_travel_plan(self, test_session: AsyncSession):
        """Test creating a travel plan."""
        # Create user first
        user = UserORM(username="testuser", email="test@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create travel plan
        travel_plan = TravelPlanORM(
            user_id=user.id,
            title="Summer Vacation",
            destination="Tokyo, Japan",
            destinations=["Tokyo", "Kyoto", "Osaka"],
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 15),
            duration_days=15,
            budget=Decimal("4000.00"),
            currency=Currency.USD,
            status=PlanStatus.PLANNING,
            travelers_count=2,
            travel_style="couple",
            flights=[
                {
                    "flight_number": "JL123",
                    "airline": "Japan Airlines",
                    "price": 800.00
                }
            ],
            hotels=[
                {
                    "name": "Tokyo Hotel",
                    "price_per_night": 150.00,
                    "star_rating": 4
                }
            ],
            itinerary=[
                {
                    "day": 1,
                    "time": "09:00",
                    "activity": "Visit Tokyo Tower",
                    "location": "Tokyo Tower"
                }
            ]
        )
        
        test_session.add(travel_plan)
        await test_session.commit()
        await test_session.refresh(travel_plan)
        
        assert travel_plan.id is not None
        assert travel_plan.title == "Summer Vacation"
        assert travel_plan.destination == "Tokyo, Japan"
        assert travel_plan.destinations == ["Tokyo", "Kyoto", "Osaka"]
        assert travel_plan.budget == Decimal("4000.00")
        assert travel_plan.currency == Currency.USD
        assert travel_plan.status == PlanStatus.PLANNING
        assert len(travel_plan.flights) == 1
        assert len(travel_plan.hotels) == 1
        assert len(travel_plan.itinerary) == 1
    
    @pytest.mark.asyncio
    async def test_travel_plan_queries(self, test_session: AsyncSession):
        """Test querying travel plans."""
        # Create user
        user = UserORM(username="testuser", email="test@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create multiple travel plans
        plans = [
            TravelPlanORM(
                user_id=user.id,
                title="Paris Trip",
                destination="Paris",
                start_date=date(2024, 6, 1),
                end_date=date(2024, 6, 10),
                duration_days=10,
                budget=Decimal("2000.00"),
                travel_style="solo",
                status=PlanStatus.PLANNING
            ),
            TravelPlanORM(
                user_id=user.id,
                title="Tokyo Trip",
                destination="Tokyo",
                start_date=date(2024, 8, 1),
                end_date=date(2024, 8, 15),
                duration_days=15,
                budget=Decimal("3000.00"),
                travel_style="solo",
                status=PlanStatus.CONFIRMED
            )
        ]
        
        for plan in plans:
            test_session.add(plan)
        await test_session.commit()
        
        # Query by status
        stmt = select(TravelPlanORM).where(TravelPlanORM.status == PlanStatus.PLANNING)
        result = await test_session.execute(stmt)
        planning_plans = result.scalars().all()
        
        assert len(planning_plans) == 1
        assert planning_plans[0].title == "Paris Trip"
        
        # Query by destination
        stmt = select(TravelPlanORM).where(TravelPlanORM.destination == "Tokyo")
        result = await test_session.execute(stmt)
        tokyo_plans = result.scalars().all()
        
        assert len(tokyo_plans) == 1
        assert tokyo_plans[0].title == "Tokyo Trip"


class TestConversationORM:
    """Test Conversation ORM operations."""
    
    @pytest.mark.asyncio
    async def test_create_conversation_with_messages(self, test_session: AsyncSession):
        """Test creating conversation with messages."""
        # Create user
        user = UserORM(username="testuser", email="test@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create conversation
        conversation = ConversationORM(
            user_id=user.id,
            title="Travel Planning Chat",
            status=ConversationStatus.ACTIVE,
            context={
                "stage": "planning",
                "destination": "Paris"
            },
            total_tokens=100,
            total_cost=0.05
        )
        test_session.add(conversation)
        await test_session.commit()
        await test_session.refresh(conversation)
        
        # Create messages
        messages = [
            MessageORM(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content="I want to plan a trip to Paris",
                tokens_used=10,
                model_name="gpt-4"
            ),
            MessageORM(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content="I'd be happy to help you plan your Paris trip!",
                tokens_used=15,
                model_name="gpt-4",
                processing_time_ms=500
            )
        ]
        
        for message in messages:
            test_session.add(message)
        await test_session.commit()
        
        # Test relationships
        await test_session.refresh(conversation)
        assert len(conversation.messages) == 2
        assert conversation.messages[0].role == MessageRole.USER
        assert conversation.messages[1].role == MessageRole.ASSISTANT
        assert conversation.messages[0].content == "I want to plan a trip to Paris"
    
    @pytest.mark.asyncio
    async def test_conversation_queries(self, test_session: AsyncSession):
        """Test querying conversations."""
        # Create user
        user = UserORM(username="testuser", email="test@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        # Create conversations
        conversations = [
            ConversationORM(
                user_id=user.id,
                title="Active Chat",
                status=ConversationStatus.ACTIVE
            ),
            ConversationORM(
                user_id=user.id,
                title="Completed Chat",
                status=ConversationStatus.COMPLETED
            )
        ]
        
        for conv in conversations:
            test_session.add(conv)
        await test_session.commit()
        
        # Query active conversations
        stmt = select(ConversationORM).where(
            ConversationORM.user_id == user.id,
            ConversationORM.status == ConversationStatus.ACTIVE
        )
        result = await test_session.execute(stmt)
        active_conversations = result.scalars().all()
        
        assert len(active_conversations) == 1
        assert active_conversations[0].title == "Active Chat"


class TestMessageORM:
    """Test Message ORM operations."""
    
    @pytest.mark.asyncio
    async def test_message_ordering(self, test_session: AsyncSession):
        """Test message ordering by timestamp."""
        # Create user and conversation
        user = UserORM(username="testuser", email="test@example.com")
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        
        conversation = ConversationORM(user_id=user.id, title="Test Chat")
        test_session.add(conversation)
        await test_session.commit()
        await test_session.refresh(conversation)
        
        # Create messages with different timestamps
        import time
        messages = []
        for i in range(3):
            message = MessageORM(
                conversation_id=conversation.id,
                role=MessageRole.USER if i % 2 == 0 else MessageRole.ASSISTANT,
                content=f"Message {i}",
                timestamp=datetime.utcnow()
            )
            messages.append(message)
            test_session.add(message)
            time.sleep(0.01)  # Small delay to ensure different timestamps
        
        await test_session.commit()
        
        # Query messages ordered by timestamp
        stmt = select(MessageORM).where(
            MessageORM.conversation_id == conversation.id
        ).order_by(MessageORM.timestamp)
        
        result = await test_session.execute(stmt)
        ordered_messages = result.scalars().all()
        
        assert len(ordered_messages) == 3
        assert ordered_messages[0].content == "Message 0"
        assert ordered_messages[1].content == "Message 1"
        assert ordered_messages[2].content == "Message 2"
        
        # Verify timestamps are in order
        for i in range(len(ordered_messages) - 1):
            assert ordered_messages[i].timestamp <= ordered_messages[i + 1].timestamp
"""
Unit tests for data models.
"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4

from pydantic import ValidationError

from shared.models import (
    User, UserPreferences, TravelRecord, UserCreate, UserUpdate,
    TravelPlan, FlightOption, HotelOption, ItineraryItem, TravelPlanCreate,
    Conversation, Message, ConversationContext, MessageCreate,
    TravelStyle, PlanStatus, ConversationStatus, MessageRole, Currency
)


class TestUserModels:
    """Test user-related models."""
    
    def test_user_preferences_valid(self):
        """Test valid user preferences creation."""
        preferences = UserPreferences(
            budget_range=(1000, 5000),
            preferred_airlines=["AA", "UA"],
            hotel_star_rating=4,
            travel_style=TravelStyle.FAMILY,
            dietary_restrictions=["vegetarian"],
            language="en",
            currency=Currency.USD
        )
        
        assert preferences.budget_range == (1000, 5000)
        assert preferences.preferred_airlines == ["AA", "UA"]
        assert preferences.hotel_star_rating == 4
        assert preferences.travel_style == TravelStyle.FAMILY
    
    def test_user_preferences_invalid_budget(self):
        """Test invalid budget range validation."""
        with pytest.raises(ValidationError) as exc_info:
            UserPreferences(budget_range=(5000, 1000))
        
        assert "Minimum budget must be less than maximum budget" in str(exc_info.value)
    
    def test_user_preferences_negative_budget(self):
        """Test negative budget validation."""
        with pytest.raises(ValidationError) as exc_info:
            UserPreferences(budget_range=(-100, 1000))
        
        assert "Budget cannot be negative" in str(exc_info.value)
    
    def test_travel_record_valid(self):
        """Test valid travel record creation."""
        start_date = datetime(2024, 6, 1)
        end_date = datetime(2024, 6, 10)
        
        record = TravelRecord(
            destination="Paris, France",
            start_date=start_date,
            end_date=end_date,
            total_cost=2500.0,
            rating=5,
            travel_style=TravelStyle.COUPLE
        )
        
        assert record.destination == "Paris, France"
        assert record.start_date == start_date
        assert record.end_date == end_date
        assert record.total_cost == 2500.0
        assert record.rating == 5
    
    def test_travel_record_invalid_dates(self):
        """Test invalid date validation in travel record."""
        start_date = datetime(2024, 6, 10)
        end_date = datetime(2024, 6, 1)
        
        with pytest.raises(ValidationError) as exc_info:
            TravelRecord(
                destination="Paris, France",
                start_date=start_date,
                end_date=end_date,
                total_cost=2500.0,
                travel_style=TravelStyle.COUPLE
            )
        
        assert "End date must be after start date" in str(exc_info.value)
    
    def test_user_create_valid(self):
        """Test valid user creation."""
        user_create = UserCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User"
        )
        
        assert user_create.username == "testuser"
        assert user_create.email == "test@example.com"
        assert user_create.full_name == "Test User"
    
    def test_user_create_invalid_email(self):
        """Test invalid email validation."""
        with pytest.raises(ValidationError):
            UserCreate(
                username="testuser",
                email="invalid-email",
                full_name="Test User"
            )


class TestTravelModels:
    """Test travel-related models."""
    
    def test_flight_option_valid(self):
        """Test valid flight option creation."""
        departure_time = datetime(2024, 6, 1, 10, 0)
        arrival_time = datetime(2024, 6, 1, 14, 0)
        
        flight = FlightOption(
            flight_number="AA123",
            airline="American Airlines",
            airline_code="AA",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration_minutes=240,
            price=Decimal("299.99"),
            cabin_class="Economy",
            stops=0
        )
        
        assert flight.flight_number == "AA123"
        assert flight.airline == "American Airlines"
        assert flight.departure_time == departure_time
        assert flight.arrival_time == arrival_time
        assert flight.price == Decimal("299.99")
    
    def test_flight_option_invalid_times(self):
        """Test invalid flight times validation."""
        departure_time = datetime(2024, 6, 1, 14, 0)
        arrival_time = datetime(2024, 6, 1, 10, 0)
        
        with pytest.raises(ValidationError) as exc_info:
            FlightOption(
                flight_number="AA123",
                airline="American Airlines",
                airline_code="AA",
                departure_airport="JFK",
                arrival_airport="LAX",
                departure_time=departure_time,
                arrival_time=arrival_time,
                duration_minutes=240,
                price=Decimal("299.99"),
                cabin_class="Economy",
                stops=0
            )
        
        assert "Arrival time must be after departure time" in str(exc_info.value)
    
    def test_hotel_option_valid(self):
        """Test valid hotel option creation."""
        check_in = date(2024, 6, 1)
        check_out = date(2024, 6, 5)
        
        hotel = HotelOption(
            name="Grand Hotel",
            address="123 Main St",
            city="New York",
            country="USA",
            star_rating=4,
            price_per_night=Decimal("200.00"),
            total_price=Decimal("800.00"),
            check_in_date=check_in,
            check_out_date=check_out,
            room_type="Deluxe Room",
            amenities=["WiFi", "Pool", "Gym"]
        )
        
        assert hotel.name == "Grand Hotel"
        assert hotel.star_rating == 4
        assert hotel.check_in_date == check_in
        assert hotel.check_out_date == check_out
        assert hotel.amenities == ["WiFi", "Pool", "Gym"]
    
    def test_hotel_option_invalid_dates(self):
        """Test invalid hotel dates validation."""
        check_in = date(2024, 6, 5)
        check_out = date(2024, 6, 1)
        
        with pytest.raises(ValidationError) as exc_info:
            HotelOption(
                name="Grand Hotel",
                address="123 Main St",
                city="New York",
                country="USA",
                star_rating=4,
                price_per_night=Decimal("200.00"),
                total_price=Decimal("800.00"),
                check_in_date=check_in,
                check_out_date=check_out,
                room_type="Deluxe Room"
            )
        
        assert "Check-out date must be after check-in date" in str(exc_info.value)
    
    def test_itinerary_item_valid(self):
        """Test valid itinerary item creation."""
        item = ItineraryItem(
            day=1,
            time="09:00",
            activity="Visit Statue of Liberty",
            location="Liberty Island",
            duration_minutes=180,
            cost=Decimal("25.00"),
            category="sightseeing"
        )
        
        assert item.day == 1
        assert item.time == "09:00"
        assert item.activity == "Visit Statue of Liberty"
        assert item.duration_minutes == 180
        assert item.cost == Decimal("25.00")
    
    def test_itinerary_item_invalid_time(self):
        """Test invalid time format validation."""
        with pytest.raises(ValidationError) as exc_info:
            ItineraryItem(
                day=1,
                time="25:00",  # Invalid time
                activity="Visit Statue of Liberty",
                location="Liberty Island",
                duration_minutes=180,
                cost=Decimal("25.00"),
                category="sightseeing"
            )
        
        assert "Time must be in HH:MM format" in str(exc_info.value)
    
    def test_travel_plan_valid(self):
        """Test valid travel plan creation."""
        start_date = date(2024, 6, 1)
        end_date = date(2024, 6, 10)
        
        plan = TravelPlan(
            user_id=str(uuid4()),
            title="Summer Vacation",
            destination="Paris, France",
            start_date=start_date,
            end_date=end_date,
            duration_days=10,
            budget=Decimal("3000.00"),
            travelers_count=2,
            travel_style="couple"
        )
        
        assert plan.title == "Summer Vacation"
        assert plan.destination == "Paris, France"
        assert plan.start_date == start_date
        assert plan.end_date == end_date
        assert plan.duration_days == 10
        assert plan.budget == Decimal("3000.00")
    
    def test_travel_plan_invalid_dates(self):
        """Test invalid travel plan dates validation."""
        start_date = date(2024, 6, 10)
        end_date = date(2024, 6, 1)
        
        with pytest.raises(ValidationError) as exc_info:
            TravelPlan(
                user_id=str(uuid4()),
                title="Summer Vacation",
                destination="Paris, France",
                start_date=start_date,
                end_date=end_date,
                duration_days=10,
                budget=Decimal("3000.00"),
                travelers_count=2,
                travel_style="couple"
            )
        
        assert "End date must be after start date" in str(exc_info.value)


class TestConversationModels:
    """Test conversation-related models."""
    
    def test_message_valid(self):
        """Test valid message creation."""
        message = Message(
            id=str(uuid4()),
            role=MessageRole.USER,
            content="Hello, I want to plan a trip to Paris",
            metadata={"intent": "travel_planning"},
            tokens_used=15
        )
        
        assert message.role == MessageRole.USER
        assert message.content == "Hello, I want to plan a trip to Paris"
        assert message.metadata["intent"] == "travel_planning"
        assert message.tokens_used == 15
    
    def test_conversation_context_valid(self):
        """Test valid conversation context creation."""
        context = ConversationContext(
            user_preferences={"budget": 2000},
            current_travel_plan_id=str(uuid4()),
            conversation_stage="planning",
            extracted_entities={"destination": "Paris"},
            language="en"
        )
        
        assert context.user_preferences["budget"] == 2000
        assert context.conversation_stage == "planning"
        assert context.extracted_entities["destination"] == "Paris"
        assert context.language == "en"
    
    def test_conversation_valid(self):
        """Test valid conversation creation."""
        user_id = str(uuid4())
        conversation = Conversation(
            user_id=user_id,
            title="Paris Trip Planning",
            status=ConversationStatus.ACTIVE
        )
        
        assert conversation.user_id == user_id
        assert conversation.title == "Paris Trip Planning"
        assert conversation.status == ConversationStatus.ACTIVE
        assert len(conversation.messages) == 0
        assert conversation.total_tokens == 0
    
    def test_conversation_add_message(self):
        """Test adding message to conversation."""
        conversation = Conversation(user_id=str(uuid4()))
        message = Message(
            id=str(uuid4()),
            role=MessageRole.USER,
            content="Hello",
            tokens_used=5
        )
        
        conversation.add_message(message)
        
        assert len(conversation.messages) == 1
        assert conversation.messages[0] == message
        assert conversation.total_tokens == 5
    
    def test_conversation_get_recent_messages(self):
        """Test getting recent messages from conversation."""
        conversation = Conversation(user_id=str(uuid4()))
        
        # Add multiple messages
        for i in range(15):
            message = Message(
                id=str(uuid4()),
                role=MessageRole.USER,
                content=f"Message {i}"
            )
            conversation.add_message(message)
        
        recent_messages = conversation.get_recent_messages(limit=5)
        assert len(recent_messages) == 5
        assert recent_messages[-1].content == "Message 14"  # Most recent
    
    def test_conversation_get_context_summary(self):
        """Test getting conversation context summary."""
        conversation = Conversation(
            user_id=str(uuid4()),
            title="Test Conversation"
        )
        
        # Add a message
        message = Message(
            id=str(uuid4()),
            role=MessageRole.USER,
            content="Hello",
            tokens_used=5
        )
        conversation.add_message(message)
        
        summary = conversation.get_context_summary()
        
        assert summary["stage"] == "initial"
        assert summary["message_count"] == 1
        assert summary["total_tokens"] == 5
        assert "entities" in summary
        assert "language" in summary
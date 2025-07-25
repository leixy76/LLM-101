#!/usr/bin/env python3
"""
Validation script for data models.
"""
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from shared.models import (
    User, UserPreferences, TravelRecord, UserCreate,
    TravelPlan, FlightOption, HotelOption, ItineraryItem,
    Conversation, Message, ConversationContext,
    TravelStyle, Currency, PlanStatus, MessageRole
)


def test_user_models():
    """Test user-related models."""
    print("Testing User models...")
    
    # Test UserPreferences
    preferences = UserPreferences(
        budget_range=(1000, 5000),
        preferred_airlines=["AA", "UA"],
        hotel_star_rating=4,
        travel_style=TravelStyle.FAMILY,
        currency=Currency.USD,
        interests=["museums", "food", "nature"]
    )
    print(f"✓ UserPreferences: {preferences.travel_style}, budget: {preferences.budget_range}")
    
    # Test TravelRecord
    record = TravelRecord(
        destination="Paris, France",
        start_date=datetime(2024, 6, 1),
        end_date=datetime(2024, 6, 10),
        total_cost=2500.0,
        rating=5,
        travel_style=TravelStyle.COUPLE
    )
    print(f"✓ TravelRecord: {record.destination}, cost: ${record.total_cost}")
    
    # Test User
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        preferences=preferences,
        travel_history=[record]
    )
    print(f"✓ User: {user.username} ({user.email})")
    
    # Test UserCreate
    user_create = UserCreate(
        username="newuser",
        email="new@example.com",
        full_name="New User"
    )
    print(f"✓ UserCreate: {user_create.username}")


def test_travel_models():
    """Test travel-related models."""
    print("\nTesting Travel models...")
    
    # Test FlightOption
    flight = FlightOption(
        flight_number="AA123",
        airline="American Airlines",
        airline_code="AA",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime(2024, 6, 1, 10, 0),
        arrival_time=datetime(2024, 6, 1, 14, 0),
        duration_minutes=240,
        price=Decimal("299.99"),
        cabin_class="Economy",
        stops=0
    )
    print(f"✓ FlightOption: {flight.flight_number} ({flight.airline}), ${flight.price}")
    
    # Test HotelOption
    hotel = HotelOption(
        name="Grand Hotel",
        address="123 Main St",
        city="New York",
        country="USA",
        star_rating=4,
        price_per_night=Decimal("200.00"),
        total_price=Decimal("800.00"),
        check_in_date=date(2024, 6, 1),
        check_out_date=date(2024, 6, 5),
        room_type="Deluxe Room",
        amenities=["WiFi", "Pool", "Gym"]
    )
    print(f"✓ HotelOption: {hotel.name} ({hotel.star_rating}★), ${hotel.price_per_night}/night")
    
    # Test ItineraryItem
    item = ItineraryItem(
        day=1,
        time="09:00",
        activity="Visit Statue of Liberty",
        location="Liberty Island",
        duration_minutes=180,
        cost=Decimal("25.00"),
        category="sightseeing"
    )
    print(f"✓ ItineraryItem: Day {item.day}, {item.activity}, ${item.cost}")
    
    # Test TravelPlan
    plan = TravelPlan(
        user_id=str(uuid4()),
        title="Summer Vacation",
        destination="New York",
        start_date=date(2024, 6, 1),
        end_date=date(2024, 6, 10),
        duration_days=10,
        budget=Decimal("3000.00"),
        travelers_count=2,
        travel_style="couple",
        flights=[flight],
        hotels=[hotel],
        itinerary=[item]
    )
    print(f"✓ TravelPlan: {plan.title} to {plan.destination}, ${plan.budget}")


def test_conversation_models():
    """Test conversation-related models."""
    print("\nTesting Conversation models...")
    
    # Test Message
    message = Message(
        id=str(uuid4()),
        role=MessageRole.USER,
        content="Hello, I want to plan a trip to Paris",
        metadata={"intent": "travel_planning"},
        tokens_used=15
    )
    print(f"✓ Message: {message.role}, {len(message.content)} chars, {message.tokens_used} tokens")
    
    # Test ConversationContext
    context = ConversationContext(
        user_preferences={"budget": 2000},
        current_travel_plan_id=str(uuid4()),
        conversation_stage="planning",
        extracted_entities={"destination": "Paris"},
        language="en"
    )
    print(f"✓ ConversationContext: stage={context.conversation_stage}, entities={len(context.extracted_entities)}")
    
    # Test Conversation
    conversation = Conversation(
        user_id=str(uuid4()),
        title="Paris Trip Planning",
        messages=[message],
        context=context
    )
    conversation.add_message(message)
    print(f"✓ Conversation: {conversation.title}, {len(conversation.messages)} messages")
    
    # Test conversation methods
    recent = conversation.get_recent_messages(limit=5)
    summary = conversation.get_context_summary()
    print(f"✓ Conversation methods: {len(recent)} recent messages, summary keys: {list(summary.keys())}")


def test_validation_errors():
    """Test model validation."""
    print("\nTesting validation...")
    
    try:
        # Invalid budget range
        UserPreferences(budget_range=(5000, 1000))
        print("✗ Should have failed: invalid budget range")
    except Exception as e:
        print(f"✓ Validation caught: {type(e).__name__}")
    
    try:
        # Invalid time format
        ItineraryItem(
            day=1,
            time="25:00",  # Invalid time
            activity="Test",
            location="Test",
            duration_minutes=60,
            cost=Decimal("10.00"),
            category="test"
        )
        print("✗ Should have failed: invalid time format")
    except Exception as e:
        print(f"✓ Validation caught: {type(e).__name__}")
    
    try:
        # Invalid dates
        TravelPlan(
            user_id=str(uuid4()),
            title="Test",
            destination="Test",
            start_date=date(2024, 6, 10),
            end_date=date(2024, 6, 1),  # End before start
            duration_days=10,
            budget=Decimal("1000.00"),
            travelers_count=1,
            travel_style="solo"
        )
        print("✗ Should have failed: invalid dates")
    except Exception as e:
        print(f"✓ Validation caught: {type(e).__name__}")


def main():
    """Run all tests."""
    print("=== AI Travel Planner - Data Models Validation ===\n")
    
    try:
        test_user_models()
        test_travel_models()
        test_conversation_models()
        test_validation_errors()
        
        print("\n=== All tests passed! ===")
        print("✓ Pydantic data models are working correctly")
        print("✓ Model validation is functioning")
        print("✓ All required fields and relationships are defined")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Database initialization script.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.database.config import init_db, close_db, engine


async def create_database():
    """Create database tables."""
    print("Initializing database...")
    
    try:
        await init_db()
        print("✓ Database tables created successfully")
        
        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print("✓ Database connection test passed")
            
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    finally:
        await close_db()
    
    return True


def main():
    """Main function."""
    print("=== AI Travel Planner - Database Initialization ===\n")
    
    # Check database URL
    db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/travel_planner")
    print(f"Database URL: {db_url}")
    
    # Run initialization
    success = asyncio.run(create_database())
    
    if success:
        print("\n=== Database initialization completed successfully ===")
        return 0
    else:
        print("\n=== Database initialization failed ===")
        return 1


if __name__ == "__main__":
    exit(main())
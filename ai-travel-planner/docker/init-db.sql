-- Initialize database for AI Travel Planner
-- This script runs when PostgreSQL container starts for the first time

-- Create additional databases if needed
-- CREATE DATABASE travel_planner_test;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create basic schema structure (will be managed by Alembic migrations)
-- This is just for initial setup

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE travel_planner TO postgres;
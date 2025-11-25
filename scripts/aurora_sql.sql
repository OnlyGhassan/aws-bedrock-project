-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID generation (recommended)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schema for Bedrock integration
CREATE SCHEMA IF NOT EXISTS bedrock_integration;

-- Create role if it doesn't exist
DO $$
BEGIN
    CREATE ROLE bedrock_user LOGIN PASSWORD 'Password123!';
EXCEPTION
    WHEN duplicate_object THEN
        RAISE NOTICE 'Role already exists';
END $$;

-- Grant access to schema
GRANT ALL ON SCHEMA bedrock_integration TO bedrock_user;

-- Create the KB table
CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    embedding vector(1536),
    chunks text,
    metadata jsonb
);

-- Create required HNSW vector index for Bedrock similarity search
CREATE INDEX IF NOT EXISTS bedrock_kb_embedding_idx
ON bedrock_integration.bedrock_kb
USING hnsw (embedding vector_cosine_ops);

-- Create REQUIRED GIN full-text index for Bedrock KB text search
CREATE INDEX IF NOT EXISTS bedrock_kb_chunks_idx
ON bedrock_integration.bedrock_kb
USING gin (to_tsvector('english', chunks));

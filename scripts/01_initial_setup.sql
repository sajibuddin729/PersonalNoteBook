-- Initial database setup for Personal Notebook
-- This script creates the necessary database structure

-- Create database (if using PostgreSQL)
-- CREATE DATABASE personal_notebook;

-- Django will handle table creation through migrations
-- This script is for any additional setup or initial data

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_notes_user_updated ON notes_note(user_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_user_pinned ON notes_note(user_id, is_pinned);
CREATE INDEX IF NOT EXISTS idx_notes_user_favorite ON notes_note(user_id, is_favorite);
CREATE INDEX IF NOT EXISTS idx_notes_category ON notes_note(category_id);
CREATE INDEX IF NOT EXISTS idx_notes_created ON notes_note(created_at);

-- Create full-text search indexes (PostgreSQL specific)
-- CREATE INDEX IF NOT EXISTS idx_notes_search ON notes_note USING gin(to_tsvector('english', title || ' ' || content));

-- Create function for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
-- (Django handles this automatically, but this is for reference)

COMMIT;

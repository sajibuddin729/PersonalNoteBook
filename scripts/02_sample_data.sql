-- Sample data for Personal Notebook
-- This script creates sample categories and note templates

-- Note: This assumes you have at least one user created
-- You should run this after creating a superuser

-- Insert sample categories (you'll need to replace user_id with actual user UUID)
-- INSERT INTO notes_category (id, name, description, color, user_id, created_at, updated_at)
-- VALUES 
--     (gen_random_uuid(), 'Work', 'Work-related notes and tasks', '#007bff', 'YOUR_USER_ID_HERE', NOW(), NOW()),
--     (gen_random_uuid(), 'Personal', 'Personal thoughts and ideas', '#28a745', 'YOUR_USER_ID_HERE', NOW(), NOW()),
--     (gen_random_uuid(), 'Projects', 'Project planning and tracking', '#ffc107', 'YOUR_USER_ID_HERE', NOW(), NOW()),
--     (gen_random_uuid(), 'Learning', 'Study notes and learning materials', '#17a2b8', 'YOUR_USER_ID_HERE', NOW(), NOW());

-- Insert sample note templates
-- INSERT INTO notes_notetemplate (id, name, template_type, content, description, is_public, user_id, created_at)
-- VALUES 
--     (gen_random_uuid(), 'Daily Standup', 'meeting', 
--      '<h2>Daily Standup - {{date}}</h2><p><strong>What I did yesterday:</strong></p><ul><li></li></ul><p><strong>What I plan to do today:</strong></p><ul><li></li></ul><p><strong>Blockers:</strong></p><ul><li></li></ul>', 
--      'Template for daily standup meetings', true, 'YOUR_USER_ID_HERE', NOW()),
--     (gen_random_uuid(), 'Weekly Review', 'journal', 
--      '<h2>Weekly Review - Week of {{date}}</h2><p><strong>Accomplishments:</strong></p><ul><li></li></ul><p><strong>Challenges:</strong></p><ul><li></li></ul><p><strong>Next week goals:</strong></p><ul><li></li></ul><p><strong>Lessons learned:</strong></p><ul><li></li></ul>', 
--      'Template for weekly review and planning', true, 'YOUR_USER_ID_HERE', NOW()),
--     (gen_random_uuid(), 'Project Kickoff', 'project', 
--      '<h2>Project: {{project_name}}</h2><p><strong>Objective:</strong></p><p><strong>Scope:</strong></p><p><strong>Timeline:</strong></p><p><strong>Team Members:</strong></p><ul><li></li></ul><p><strong>Key Milestones:</strong></p><ul><li></li></ul><p><strong>Risks:</strong></p><ul><li></li></ul>', 
--      'Template for project kickoff documentation', true, 'YOUR_USER_ID_HERE', NOW());

-- Create some sample notes (replace with actual user ID)
-- INSERT INTO notes_note (id, title, content, priority, is_pinned, is_favorite, user_id, created_at, updated_at)
-- VALUES 
--     (gen_random_uuid(), 'Welcome to Personal Notebook!', 
--      '<h2>Getting Started</h2><p>Welcome to your personal notebook! Here are some tips to get you started:</p><ul><li>Create categories to organize your notes</li><li>Use tags to make notes searchable</li><li>Pin important notes to keep them at the top</li><li>Use the rich text editor for formatting</li></ul><p>Happy note-taking!</p>', 
--      'medium', true, true, 'YOUR_USER_ID_HERE', NOW(), NOW());

COMMIT;

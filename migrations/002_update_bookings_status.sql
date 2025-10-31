-- File: 002_update_booking_status.sql
-- Date: January 2024
-- What: Updated booking status ENUM and values
-- Why: Needed better workflow (accept/reject instead of confirm/cancel)

-- Changes made:
-- 1. Changed 'confirmed' status to 'accepted'
-- 2. Changed 'cancelled' status to 'rejected'  
-- 3. Updated ENUM to: pending, accepted, in_progress, completed, rejected

-- Note: This change was already applied manually
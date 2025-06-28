#!/usr/bin/env python3
"""
Database migration script to remove unique constraints from roll_call fields
This allows multiple students/mentors to have the same roll call class (e.g., 12/7, 8G)
"""

import os
import sys
import sqlite3
from datetime import datetime

def migrate_database():
    """Remove unique constraints from roll_call fields"""
    
    # Get database path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'mentorship.db')
    
    if not os.path.exists(db_path):
        print("✅ No existing database found - constraints will be correct in new database")
        return
    
    print("🔧 Migrating database to remove unique constraints...")
    
    try:
        # Create backup
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.system(f"cp '{db_path}' '{backup_path}'")
        print(f"📦 Created backup: {backup_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if we need to migrate
        cursor.execute("PRAGMA table_info(mentor)")
        mentor_columns = cursor.fetchall()
        
        # Create new mentor table without unique constraint
        cursor.execute('''
            CREATE TABLE mentor_new (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                roll_call VARCHAR(20) NOT NULL,
                role VARCHAR(50) DEFAULT 'Mentor',
                subjects VARCHAR(200) NOT NULL,
                max_mentees INTEGER DEFAULT 5,
                start_date DATE,
                term VARCHAR(20),
                week VARCHAR(20),
                day VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Copy data from old table
        cursor.execute('''
            INSERT INTO mentor_new (id, name, roll_call, subjects, max_mentees, created_at)
            SELECT id, name, roll_call, subjects, max_mentees, created_at FROM mentor
        ''')
        
        # Drop old table and rename new table
        cursor.execute('DROP TABLE mentor')
        cursor.execute('ALTER TABLE mentor_new RENAME TO mentor')
        
        # Create new mentee table without unique constraint
        cursor.execute('''
            CREATE TABLE mentee_new (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                roll_call VARCHAR(20) NOT NULL,
                subject VARCHAR(50) NOT NULL,
                lessons_remaining INTEGER DEFAULT 0,
                mentor_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mentor_id) REFERENCES mentor (id)
            )
        ''')
        
        # Copy data from old table
        cursor.execute('''
            INSERT INTO mentee_new (id, name, roll_call, subject, lessons_remaining, mentor_id, created_at)
            SELECT id, name, roll_call, subject, lessons_remaining, mentor_id, created_at FROM mentee
        ''')
        
        # Drop old table and rename new table
        cursor.execute('DROP TABLE mentee')
        cursor.execute('ALTER TABLE mentee_new RENAME TO mentee')
        
        # Recreate session table to maintain foreign key relationships
        cursor.execute('''
            CREATE TABLE session_new (
                id INTEGER PRIMARY KEY,
                mentor_id INTEGER NOT NULL,
                mentee_id INTEGER NOT NULL,
                date DATE NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                duration_minutes INTEGER NOT NULL,
                subject VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'scheduled',
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mentor_id) REFERENCES mentor (id),
                FOREIGN KEY (mentee_id) REFERENCES mentee (id)
            )
        ''')
        
        # Check if session table exists and copy data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='session'")
        if cursor.fetchone():
            cursor.execute('''
                INSERT INTO session_new (id, mentor_id, mentee_id, date, start_time, end_time, duration_minutes, subject, status, notes, created_at)
                SELECT id, mentor_id, mentee_id, date, start_time, end_time, duration_minutes, subject, status, notes, created_at FROM session
            ''')
            cursor.execute('DROP TABLE session')
        
        cursor.execute('ALTER TABLE session_new RENAME TO session')
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        print("🎓 Multiple students can now have the same roll call class")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Restore backup if it exists
        if 'backup_path' in locals() and os.path.exists(backup_path):
            os.system(f"cp '{backup_path}' '{db_path}'")
            print(f"🔄 Restored backup from {backup_path}")
        sys.exit(1)

if __name__ == '__main__':
    migrate_database()

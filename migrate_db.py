#!/usr/bin/env python3
"""
Database migration script to add new mentor fields
This script adds the new columns to existing mentor records
"""
import os
import sys
import sqlite3
from datetime import datetime

def migrate_database():
    """Add new columns to the mentor table"""
    
    # Database path
    db_path = 'mentorship.db'
    if not os.path.exists(db_path):
        print("✅ No existing database found - new database will be created with all fields")
        return True
    
    print("🔧 Migrating existing database...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(mentor)")
        columns = [row[1] for row in cursor.fetchall()]
        
        new_columns = [
            ('first_name', 'VARCHAR(50)'),
            ('last_name', 'VARCHAR(50)'),
            ('role', 'VARCHAR(50) DEFAULT "Mentor"'),
            ('start_date', 'DATE'),
            ('term', 'VARCHAR(20)'),
            ('week', 'VARCHAR(20)'),
            ('day', 'VARCHAR(20)')
        ]
        
        # Add missing columns
        for column_name, column_type in new_columns:
            if column_name not in columns:
                print(f"  Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE mentor ADD COLUMN {column_name} {column_type}")
        
        # Update existing records - split name into first_name and last_name
        cursor.execute("SELECT id, name FROM mentor WHERE first_name IS NULL OR last_name IS NULL")
        mentors = cursor.fetchall()
        
        for mentor_id, full_name in mentors:
            if full_name:
                name_parts = full_name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                cursor.execute("""
                    UPDATE mentor 
                    SET first_name = ?, last_name = ?, role = COALESCE(role, 'Mentor')
                    WHERE id = ?
                """, (first_name, last_name, mentor_id))
                
                print(f"  Updated mentor: {full_name} -> {first_name} {last_name}")
        
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1)

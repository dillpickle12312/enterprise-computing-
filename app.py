#!/usr/bin/env python3
"""
Mentorship System - Main Flask Application
A comprehensive web application for managing mentor-mentee relationships,
scheduling sessions, and tracking progress in educational settings.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import csv
import io
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration using environment variables with fallbacks
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "mentorship.db")}'

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Mentor(db.Model):
    """Mentor model representing tutors/teachers"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_call = db.Column(db.String(20), unique=True, nullable=False)
    subjects = db.Column(db.String(200), nullable=False)  # Comma-separated subjects
    max_mentees = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    mentees = db.relationship('Mentee', backref='assigned_mentor', lazy=True)
    sessions = db.relationship('Session', backref='mentor', lazy=True)
    
    def get_subjects_list(self):
        """Return subjects as a list"""
        return [s.strip() for s in self.subjects.split(',') if s.strip()]
    
    def current_mentee_count(self):
        """Return current number of assigned mentees"""
        return len([m for m in self.mentees if m.mentor_id == self.id])
    
    def can_take_more_mentees(self):
        """Check if mentor can take more mentees"""
        return self.current_mentee_count() < self.max_mentees
    
    def __repr__(self):
        return f'<Mentor {self.name}>'

class Mentee(db.Model):
    """Mentee model representing students"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_call = db.Column(db.String(20), unique=True, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    lessons_remaining = db.Column(db.Integer, default=0)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='mentee', lazy=True)
    
    def get_total_lessons(self):
        """Get total lessons for the subject"""
        lesson_counts = {'Math': 7, 'English': 7, 'Science': 3, 'Chess': 6}
        return lesson_counts.get(self.subject, 5)
    
    def get_completed_lessons(self):
        """Calculate completed lessons"""
        return self.get_total_lessons() - self.lessons_remaining
    
    def get_progress_percentage(self):
        """Calculate progress percentage"""
        total = self.get_total_lessons()
        if total == 0:
            return 0
        return round((self.get_completed_lessons() / total) * 100)
    
    def is_completed(self):
        """Check if all lessons are completed"""
        return self.lessons_remaining <= 0
    
    def __repr__(self):
        return f'<Mentee {self.name}>'

class Session(db.Model):
    """Session model representing scheduled mentoring sessions"""
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_datetime_start(self):
        """Get combined datetime for start"""
        return datetime.combine(self.date, self.start_time)
    
    def get_datetime_end(self):
        """Get combined datetime for end"""
        return datetime.combine(self.date, self.end_time)
    
    def is_today(self):
        """Check if session is today"""
        return self.date == datetime.now().date()
    
    def is_past(self):
        """Check if session is in the past"""
        return self.get_datetime_start() < datetime.now()
    
    def __repr__(self):
        return f'<Session {self.mentor.name} -> {self.mentee.name} on {self.date}>'

# Routes
@app.route('/')
def dashboard():
    """Dashboard route showing overview statistics"""
    today = datetime.now().date()
    
    # Basic counts
    total_mentors = Mentor.query.count()
    total_mentees = Mentee.query.count()
    total_sessions = Session.query.count()
    
    # Session statistics by status
    sessions_scheduled = Session.query.filter_by(status='scheduled').count()
    sessions_completed = Session.query.filter_by(status='completed').count()
    sessions_canceled = Session.query.filter_by(status='cancelled').count()
    
    # Additional session stats (these might not exist yet, so default to 0)
    sessions_rescheduled = 0  # This would need a 'rescheduled' status if implemented
    sessions_missed = 0  # This would need a 'missed' status if implemented
    
    # Mentee statistics
    assigned_mentees = Mentee.query.filter(Mentee.mentor_id.isnot(None)).count()
    unassigned_mentees = Mentee.query.filter_by(mentor_id=None).count()
    
    # Calculate mentees who graduated today (completed all lessons)
    graduated_today = 0
    for mentee in Mentee.query.all():
        if mentee.is_completed():
            # Check if they have a session today that would mark completion
            today_sessions = Session.query.filter_by(
                mentee_id=mentee.id, 
                date=today,
                status='completed'
            ).count()
            if today_sessions > 0:
                graduated_today += 1
    
    # Calculate mentors near retirement (those with 5-6 completed sessions)
    mentors_near_retirement = 0
    for mentor in Mentor.query.all():
        completed_sessions_count = Session.query.filter_by(
            mentor_id=mentor.id,
            status='completed'
        ).count()
        if 5 <= completed_sessions_count <= 6:
            mentors_near_retirement += 1
    
    stats = {
        'total_mentors': total_mentors,
        'total_mentees': total_mentees,
        'total_sessions': total_sessions,
        'sessions_scheduled': sessions_scheduled,
        'sessions_completed': sessions_completed,
        'sessions_canceled': sessions_canceled,
        'sessions_rescheduled': sessions_rescheduled,
        'sessions_missed': sessions_missed,
        'completed_sessions': sessions_completed,  # Alias for backward compatibility
        'assigned_mentees': assigned_mentees,
        'unassigned_mentees': unassigned_mentees,
        'graduated_today': graduated_today,
        'mentors_near_retirement': mentors_near_retirement
    }
    
    # Recent sessions
    recent_sessions = Session.query.order_by(Session.created_at.desc()).limit(5).all()
    
    # Sessions due today
    sessions_today = Session.query.filter_by(date=today).all()
      # Subject statistics
    subject_stats = {}
    lessons_by_subject = {}
    mentees = Mentee.query.all()
    for mentee in mentees:
        if mentee.subject not in subject_stats:
            subject_stats[mentee.subject] = {'total': 0, 'completed': 0, 'in_progress': 0}
            lessons_by_subject[mentee.subject] = 0
        
        subject_stats[mentee.subject]['total'] += 1
        if mentee.is_completed():
            subject_stats[mentee.subject]['completed'] += 1
        else:
            subject_stats[mentee.subject]['in_progress'] += 1
          # Calculate completed lessons for this mentee
        completed_lessons = mentee.get_completed_lessons()
        lessons_by_subject[mentee.subject] += completed_lessons
    
    # Get recent mentors and mentees for dashboard display
    recent_mentors = Mentor.query.order_by(
        Mentor.created_at.desc()).limit(5).all()
    recent_mentees = Mentee.query.order_by(
        Mentee.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                           stats=stats,
                           recent_sessions=recent_sessions,
                           today_sessions=sessions_today,
                           subject_stats=subject_stats,
                           lessons_by_subject=lessons_by_subject,
                           mentors=recent_mentors,
                           mentees=recent_mentees)

@app.route('/mentors')
def mentors():
    """View all mentors"""
    mentors_list = Mentor.query.all()
    
    # Calculate enhanced mentor data for the template
    mentor_data = []
    for mentor in mentors_list:
        # Count completed sessions (sessions in the past or completed)
        completed_sessions = Session.query.filter_by(
            mentor_id=mentor.id,
            status='completed'
        ).count()
        
        # Calculate status and progress
        remaining_sessions = max(0, 7 - completed_sessions)
        progress_percentage = min(100, (completed_sessions / 7) * 100)
        
        # Determine status and color
        if completed_sessions == 0:
            status = "ACTIVE"
            status_class = "success"
        elif completed_sessions <= 2:
            status = "ACTIVE"
            status_class = "success"
        elif completed_sessions <= 4:
            status = "MID-TERM"
            status_class = "info"
        elif completed_sessions == 5:
            status = "NEAR RETIREMENT"
            status_class = "warning"
        elif completed_sessions == 6:
            status = "CRITICAL"
            status_class = "warning"
        else:
            status = "RETIRED"
            status_class = "danger"
        
        mentor_data.append({
            'mentor': mentor,
            'completed_sessions': completed_sessions,
            'remaining_sessions': remaining_sessions,
            'progress_percentage': progress_percentage,
            'status': status,
            'status_class': status_class
        })
    
    return render_template('mentors.html', mentor_data=mentor_data)

@app.route('/add_mentor', methods=['GET', 'POST'])
def add_mentor():
    """Add a new mentor"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        roll_call = request.form['roll_call'].strip()
        subjects = request.form['subjects'].strip()
        max_mentees = int(request.form['max_mentees'])
        
        # Check if roll_call already exists
        if Mentor.query.filter_by(roll_call=roll_call).first():
            flash(f'Mentor with roll call {roll_call} already exists!', 'error')
            return render_template('add_mentor.html')
        
        mentor = Mentor(
            name=name,
            roll_call=roll_call,
            subjects=subjects,
            max_mentees=max_mentees
        )
        
        try:
            db.session.add(mentor)
            db.session.commit()
            flash(f'Mentor {name} added successfully!', 'success')
            return redirect(url_for('mentors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding mentor: {str(e)}', 'error')
    
    return render_template('add_mentor.html')

@app.route('/mentor/<int:id>')
def mentor_detail(id):
    """View mentor details"""
    mentor = Mentor.query.get_or_404(id)
    return render_template('mentor_detail.html', mentor=mentor)

@app.route('/delete_mentor/<int:id>')
def delete_mentor_confirm(id):
    """Confirm mentor deletion"""
    mentor = Mentor.query.get_or_404(id)
    return render_template('delete_mentor_confirm.html', mentor=mentor)

@app.route('/delete_mentor/<int:id>/confirm', methods=['POST'])
def delete_mentor(id):
    """Delete a mentor"""
    mentor = Mentor.query.get_or_404(id)
    
    try:
        # Unassign all mentees
        for mentee in mentor.mentees:
            mentee.mentor_id = None
        
        # Delete associated sessions
        Session.query.filter_by(mentor_id=id).delete()
        
        # Delete mentor
        db.session.delete(mentor)
        db.session.commit()
        flash(f'Mentor {mentor.name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting mentor: {str(e)}', 'error')
    
    return redirect(url_for('mentors'))

@app.route('/mentees')
def mentees():
    """View all mentees"""
    mentees_list = Mentee.query.all()
    return render_template('mentees.html', mentees=mentees_list)

@app.route('/add_mentee', methods=['GET', 'POST'])
def add_mentee():
    """Add a new mentee"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        roll_call = request.form['roll_call'].strip()
        subject = request.form['subject']
        
        # Check if roll_call already exists
        if Mentee.query.filter_by(roll_call=roll_call).first():
            flash(f'Mentee with roll call {roll_call} already exists!', 'error')
            return render_template('add_mentee.html')
        
        # Set lessons based on subject
        lesson_counts = {'Math': 7, 'English': 7, 'Science': 3, 'Chess': 6}
        lessons_remaining = lesson_counts.get(subject, 5)
        
        mentee = Mentee(
            name=name,
            roll_call=roll_call,
            subject=subject,
            lessons_remaining=lessons_remaining
        )
        
        try:
            db.session.add(mentee)
            db.session.commit()
            flash(f'Mentee {name} added successfully!', 'success')
            return redirect(url_for('mentees'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding mentee: {str(e)}', 'error')
    
    return render_template('add_mentee.html')

@app.route('/mentee/<int:id>')
def mentee_detail(id):
    """View mentee details"""
    mentee = Mentee.query.get_or_404(id)
    return render_template('mentee_detail.html', mentee=mentee)

@app.route('/delete_mentee/<int:id>')
def delete_mentee_confirm(id):
    """Confirm mentee deletion"""
    mentee = Mentee.query.get_or_404(id)
    return render_template('delete_mentee_confirm.html', mentee=mentee)

@app.route('/delete_mentee/<int:id>/confirm', methods=['POST'])
def delete_mentee(id):
    """Delete a mentee"""
    mentee = Mentee.query.get_or_404(id)
    
    try:
        # Delete associated sessions
        Session.query.filter_by(mentee_id=id).delete()
        
        # Delete mentee
        db.session.delete(mentee)
        db.session.commit()
        flash(f'Mentee {mentee.name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting mentee: {str(e)}', 'error')
    
    return redirect(url_for('mentees'))

@app.route('/assign_mentor', methods=['GET', 'POST'])
def assign_mentor():
    """Assign mentor to mentee"""
    if request.method == 'POST':
        mentee_id = int(request.form['mentee_id'])
        mentor_id = int(request.form['mentor_id'])
        
        mentee = Mentee.query.get_or_404(mentee_id)
        mentor = Mentor.query.get_or_404(mentor_id)
        
        # Check if mentor can teach the subject
        if mentee.subject not in mentor.get_subjects_list():
            flash(f'Mentor {mentor.name} cannot teach {mentee.subject}!', 'error')
            return redirect(url_for('assign_mentor'))
        
        # Check mentor capacity
        if not mentor.can_take_more_mentees():
            flash(f'Mentor {mentor.name} has reached maximum capacity!', 'error')
            return redirect(url_for('assign_mentor'))
        
        try:
            mentee.mentor_id = mentor_id
            db.session.commit()
            flash(f'Successfully assigned {mentor.name} to {mentee.name}!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error assigning mentor: {str(e)}', 'error')
        
        return redirect(url_for('assign_mentor'))
      # Get unassigned mentees and available mentors
    unassigned_mentees = Mentee.query.filter_by(mentor_id=None).all()
    mentors_list = Mentor.query.all()
      # Create JSON-serializable mentor data for the template
    available_mentors = []
    for mentor in mentors_list:
        mentor_info = {
            'mentor': {
                'id': mentor.id,
                'name': mentor.name,
                'roll_call': mentor.roll_call,
                'subjects': mentor.subjects,
                'max_mentees': mentor.max_mentees,
                'mentees': [{'id': m.id, 'name': m.name} for m in mentor.mentees]
            },
            'can_take_more': mentor.can_take_more_mentees(),
            'current_count': mentor.current_mentee_count()
        }
        available_mentors.append(mentor_info)
    
    return render_template('assign_mentor.html', 
                         unassigned_mentees=unassigned_mentees, 
                         mentors=mentors_list,
                         available_mentors=available_mentors)

@app.route('/calendar')
def calendar():
    """Calendar view for sessions"""
    sessions = Session.query.all()
    today = datetime.now().date()
    return render_template('calendar.html', sessions=sessions, today=today)

@app.route('/schedule_session', methods=['GET', 'POST'])
def schedule_session():
    """Schedule a new session"""
    if request.method == 'POST':
        # Handle both types of form submissions
        if 'mentor_mentee_pair' in request.form and request.form['mentor_mentee_pair']:
            # Pair-based scheduling (existing workflow)
            pair_data = request.form['mentor_mentee_pair'].split(',')
            mentor_id = int(pair_data[0])
            mentee_id = int(pair_data[1])
            date = datetime.strptime(request.form['scheduled_date'], '%Y-%m-%d').date()
            start_time = datetime.strptime('12:30', '%H:%M').time()  # Fixed lunch time
            duration = 45  # Fixed 45 minutes
        else:
            # Direct scheduling (new flexible workflow)
            mentor_id = int(request.form['mentor_id'])
            mentee_id = int(request.form['mentee_id'])
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(request.form.get('start_time', '12:30'), '%H:%M').time()
            duration = int(request.form.get('duration', 45))
        
        # Calculate end time
        start_datetime = datetime.combine(date, start_time)
        end_datetime = start_datetime + timedelta(minutes=duration)
        end_time = end_datetime.time()
        
        mentor = Mentor.query.get_or_404(mentor_id)
        mentee = Mentee.query.get_or_404(mentee_id)
        
        # Validation: Check if mentor can teach the subject
        if mentee.subject not in mentor.get_subjects_list():
            flash(f'Error: {mentor.name} cannot teach {mentee.subject}!', 'error')
            return redirect(url_for('schedule_session'))
        
        # Validation: Check mentor session limit
        session_count = Session.query.filter_by(mentor_id=mentor.id).count()
        if session_count >= 7:
            flash(f'Error: {mentor.name} has reached the maximum of 7 sessions!', 'error')
            return redirect(url_for('schedule_session'))
        
        # Validation: Check mentee lesson limit
        if mentee.lessons_remaining <= 0:
            flash(f'Error: {mentee.name} has no lessons remaining!', 'error')
            return redirect(url_for('schedule_session'))
        
        session = Session(
            mentor_id=mentor_id,
            mentee_id=mentee_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration,
            subject=mentee.subject
        )
        
        try:
            db.session.add(session)
            
            # If mentee wasn't assigned to this mentor, assign them automatically
            if mentee.mentor_id != mentor_id:
                mentee.mentor_id = mentor_id
                flash(f'Note: {mentee.name} has been automatically assigned to {mentor.name}.', 'info')
            
            # Decrease lessons remaining
            mentee.lessons_remaining = max(0, mentee.lessons_remaining - 1)
            
            db.session.commit()
            flash(f'Session scheduled successfully between {mentor.name} and {mentee.name}!', 'success')
            return redirect(url_for('calendar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling session: {str(e)}', 'error')
    
    # Get all mentors and mentees
    mentors_list = Mentor.query.all()
    all_mentees = Mentee.query.all()
    
    # Filter available mentors (those who can still conduct sessions)
    available_mentors = []
    for mentor in mentors_list:
        # Count sessions for this mentor
        session_count = Session.query.filter_by(mentor_id=mentor.id).count()
        mentor.lessons_left = max(0, 7 - session_count)  # Add lessons_left attribute
        if mentor.lessons_left > 0:
            available_mentors.append(mentor)
    
    # Get unassigned mentees (those without mentors)
    unassigned_mentees = Mentee.query.filter_by(mentor_id=None).all()
    
    # Filter available mentees (those with lessons remaining)
    available_mentees = []
    for mentee in all_mentees:
        if mentee.lessons_remaining > 0:
            available_mentees.append(mentee)
    
    # Create mentor-mentee pairs for easy scheduling (assigned pairs)
    pairs = []
    for mentor in available_mentors:
        # Get mentees assigned to this mentor
        assigned_mentees = Mentee.query.filter_by(mentor_id=mentor.id).all()
        for mentee in assigned_mentees:
            if mentee.lessons_remaining > 0:  # Only include if mentee has lessons left
                pairs.append({
                    'mentor': mentor,
                    'mentee': mentee
                })
    
    # Create potential pairs for flexible scheduling (any compatible mentor-mentee)
    flexible_pairs = []
    for mentor in available_mentors:
        mentor_subjects = mentor.get_subjects_list()
        for mentee in available_mentees:
            if mentee.subject in mentor_subjects:
                flexible_pairs.append({
                    'mentor': mentor,
                    'mentee': mentee,
                    'is_assigned': mentee.mentor_id == mentor.id
                })
    
    return render_template('schedule_session.html', 
                           mentors=mentors_list,
                           available_mentors=available_mentors,
                           unassigned_mentees=unassigned_mentees,
                           available_mentees=available_mentees,
                           pairs=pairs,
                           flexible_pairs=flexible_pairs)

@app.route('/reschedule_session', methods=['POST'])
def reschedule_session():
    """Reschedule an existing session"""
    session_id = request.form.get('session_id')
    new_date = request.form.get('new_date')
    new_time = request.form.get('new_time')
    
    try:
        session = Session.query.get_or_404(session_id)
        
        # Update session date and time
        if new_date:
            session.date = datetime.strptime(new_date, '%Y-%m-%d').date()
        
        if new_time:
            session.start_time = datetime.strptime(new_time, '%H:%M').time()
            # Calculate end time (assuming 1 hour duration)
            end_datetime = datetime.combine(session.date, session.start_time) + timedelta(hours=1)
            session.end_time = end_datetime.time()
        
        db.session.commit()
        flash('Session rescheduled successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error rescheduling session: {str(e)}', 'error')
    
    return redirect(url_for('calendar'))

@app.route('/api/sessions')
def api_sessions():
    """API endpoint for calendar events"""
    sessions = Session.query.all()
    events = []
    
    for session in sessions:
        color = '#28a745' if session.status == 'completed' else '#007bff'
        if session.status == 'cancelled':
            color = '#dc3545'
        
        events.append({
            'id': session.id,
            'title': f'{session.mentor.name} → {session.mentee.name}',
            'start': session.get_datetime_start().isoformat(),
            'end': session.get_datetime_end().isoformat(),
            'color': color,
            'extendedProps': {
                'mentor': session.mentor.name,
                'mentee': session.mentee.name,
                'subject': session.subject,
                'status': session.status
            }
        })
    
    return jsonify(events)

@app.route('/user_guide')
def user_guide():
    """User guide page"""
    return render_template('user_guide.html')

@app.route('/clear_all_data')
def clear_all_data():
    """Clear all data confirmation page"""
    return render_template('clear_all_data.html')

@app.route('/clear_all_data/confirm', methods=['POST'])
def clear_all_data_confirm():
    """Clear all data from database"""
    try:
        Session.query.delete()
        Mentee.query.delete()
        Mentor.query.delete()
        db.session.commit()
        flash('All data cleared successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing data: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/export_data/<data_type>')
def export_data(data_type):
    """Export data as CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    if data_type == 'mentors':
        # Export mentors
        writer.writerow(['ID', 'Name', 'Roll Call', 'Subjects', 'Max Mentees', 'Current Mentees', 'Created At'])
        mentors = Mentor.query.all()
        for mentor in mentors:
            writer.writerow([
                mentor.id,
                mentor.name,
                mentor.roll_call,
                mentor.subjects,
                mentor.max_mentees,
                mentor.current_mentee_count(),
                mentor.created_at.strftime('%Y-%m-%d %H:%M:%S') if mentor.created_at else ''
            ])
        filename = 'mentors_export.csv'
        
    elif data_type == 'mentees':
        # Export mentees
        writer.writerow(['ID', 'Name', 'Roll Call', 'Subject', 'Lessons Remaining', 'Assigned Mentor', 'Progress %', 'Created At'])
        mentees = Mentee.query.all()
        for mentee in mentees:
            mentor_name = mentee.assigned_mentor.name if mentee.assigned_mentor else 'Not Assigned'
            writer.writerow([
                mentee.id,
                mentee.name,
                mentee.roll_call,
                mentee.subject,
                mentee.lessons_remaining,
                mentor_name,
                mentee.get_progress_percentage(),
                mentee.created_at.strftime('%Y-%m-%d %H:%M:%S') if mentee.created_at else ''
            ])
        filename = 'mentees_export.csv'
        
    elif data_type == 'sessions':
        # Export sessions
        writer.writerow(['ID', 'Mentor', 'Mentee', 'Date', 'Start Time', 'End Time', 'Duration (min)', 'Subject', 'Status', 'Notes', 'Created At'])
        sessions = Session.query.all()
        for session in sessions:
            writer.writerow([
                session.id,
                session.mentor.name,
                session.mentee.name,
                session.date.strftime('%Y-%m-%d') if session.date else '',
                session.start_time.strftime('%H:%M') if session.start_time else '',
                session.end_time.strftime('%H:%M') if session.end_time else '',
                session.duration_minutes,
                session.subject,
                session.status,
                session.notes or '',
                session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else ''
            ])
        filename = 'sessions_export.csv'
        
    else:
        flash('Invalid export type!', 'error')
        return redirect(url_for('dashboard'))
    
    # Create response
    output.seek(0)
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
    return response

@app.route('/reassign_mentees')
@app.route('/reassign_mentees/<int:mentor_id>', methods=['GET', 'POST'])
def reassign_mentees(mentor_id=None):
    """Reassign mentees from one mentor to another"""
    if not mentor_id:
        # General reassignment interface - redirect to mentors list for now
        flash('Please select a mentor to reassign mentees from.', 'info')
        return redirect(url_for('mentors'))
    
    mentor = Mentor.query.get_or_404(mentor_id)
    
    if request.method == 'POST':
        # Handle reassignment form submission
        reassignments = request.form.getlist('reassignments')
        hidden_mentor_id = request.form.get('from_mentor_id', mentor_id)
        
        if not reassignments:
            flash('No reassignments selected!', 'warning')
            return redirect(url_for('reassign_mentees', mentor_id=mentor_id))
        
        try:
            reassigned_count = 0
            for assignment in reassignments:
                if assignment:  # Skip empty selections
                    try:
                        mentee_id, to_mentor_id = assignment.split('-')
                        mentee = Mentee.query.get(int(mentee_id))
                        to_mentor = Mentor.query.get(int(to_mentor_id))
                        
                        if mentee and to_mentor and mentee.mentor_id == mentor.id:
                            # Check if target mentor can teach the subject
                            if mentee.subject in to_mentor.get_subjects_list():
                                # Check capacity
                                if to_mentor.can_take_more_mentees():
                                    mentee.mentor_id = to_mentor.id
                                    reassigned_count += 1
                                else:
                                    flash(f'Cannot reassign {mentee.name}: {to_mentor.name} has reached capacity!', 'warning')
                            else:
                                flash(f'Cannot reassign {mentee.name}: {to_mentor.name} cannot teach {mentee.subject}!', 'warning')
                    except ValueError:
                        continue  # Skip invalid format
            
            db.session.commit()
            if reassigned_count > 0:
                flash(f'Successfully reassigned {reassigned_count} mentee(s) from {mentor.name}!', 'success')
                return redirect(url_for('mentor_detail', id=mentor_id))
            else:
                flash('No mentees were reassigned!', 'warning')
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error reassigning mentees: {str(e)}', 'error')
      # GET request - show the reassignment form
    # Get mentees assigned to this mentor
    assigned_mentees = Mentee.query.filter_by(mentor_id=mentor_id).all()
    
    # Calculate lessons left for the mentor (assuming 7 is the retirement limit)
    completed_sessions = Session.query.filter_by(
        mentor_id=mentor_id, 
        status='completed'
    ).count()
    mentor.lessons_left = max(0, 7 - completed_sessions)
    
    # Get potential target mentors (excluding the current mentor)
    target_mentors = Mentor.query.filter(Mentor.id != mentor_id).all()
    
    # Calculate mentor info with capacity and compatibility
    available_mentors = []
    for target_mentor in target_mentors:
        available_slots = target_mentor.max_mentees - target_mentor.current_mentee_count()
        if available_slots > 0:  # Only include mentors with available capacity
            available_mentors.append({
                'mentor': target_mentor,
                'available_slots': available_slots,
                'compatible_subjects': target_mentor.get_subjects_list()
            })
    
    return render_template('reassign_mentees.html', 
                         mentor=mentor, 
                         assigned_mentees=assigned_mentees,
                         available_mentors=available_mentors)

@app.route('/reassign_mentees_action', methods=['POST'])
def reassign_mentees_action():
    """Handle the actual reassignment action"""
    from_mentor_id = request.form.get('from_mentor_id')
    assignments = []
    
    # Parse the form data for reassignments
    for key, value in request.form.items():
        if key.startswith('mentee_') and value:
            mentee_id = key.replace('mentee_', '')
            to_mentor_id = value
            assignments.append((mentee_id, to_mentor_id))
    
    if not assignments:
        flash('No reassignments selected!', 'warning')
        return redirect(url_for('reassign_mentees', mentor_id=from_mentor_id))
    
    from_mentor = Mentor.query.get_or_404(from_mentor_id)
    
    try:
        reassigned_count = 0
        for mentee_id, to_mentor_id in assignments:
            mentee = Mentee.query.get(mentee_id)
            to_mentor = Mentor.query.get(to_mentor_id)
            
            if mentee and to_mentor and mentee.mentor_id == int(from_mentor_id):
                # Check if target mentor can teach the subject
                if mentee.subject in to_mentor.get_subjects_list():
                    # Check capacity
                    if to_mentor.can_take_more_mentees():
                        mentee.mentor_id = int(to_mentor_id)
                        reassigned_count += 1
                    else:
                        flash(f'Cannot reassign {mentee.name}: {to_mentor.name} has reached capacity!', 'warning')
                else:
                    flash(f'Cannot reassign {mentee.name}: {to_mentor.name} cannot teach {mentee.subject}!', 'warning')
        
        db.session.commit()
        if reassigned_count > 0:
            flash(f'Successfully reassigned {reassigned_count} mentee(s) from {from_mentor.name}!', 'success')
        else:
            flash('No mentees were reassigned!', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error reassigning mentees: {str(e)}', 'error')
    
    return redirect(url_for('mentor_detail', id=from_mentor_id))


@app.route('/bulk_assign_mentors', methods=['GET', 'POST'])
def bulk_assign_mentors():
    """Bulk assign mentors to multiple unassigned mentees"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'auto_assign':
            # Auto-assign unassigned mentees to available mentors
            unassigned_mentees = Mentee.query.filter_by(mentor_id=None).all()
            assigned_count = 0
            
            try:
                for mentee in unassigned_mentees:
                    # Find available mentors who can teach this subject
                    available_mentors = []
                    for mentor in Mentor.query.all():
                        if (mentee.subject in mentor.get_subjects_list() and 
                            mentor.can_take_more_mentees()):
                            available_mentors.append(mentor)
                    
                    if available_mentors:
                        # Choose mentor with least current mentees
                        best_mentor = min(available_mentors, key=lambda m: m.current_mentee_count())
                        mentee.mentor_id = best_mentor.id
                        assigned_count += 1
                
                db.session.commit()
                flash(f'Successfully auto-assigned {assigned_count} mentee(s)!', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error auto-assigning mentees: {str(e)}', 'error')
        
        else:
            # Manual bulk assignment
            assignments = []
            for key, value in request.form.items():
                if key.startswith('mentee_') and value:
                    mentee_id = key.replace('mentee_', '')
                    mentor_id = value
                    assignments.append((mentee_id, mentor_id))
            
            try:
                assigned_count = 0
                for mentee_id, mentor_id in assignments:
                    mentee = Mentee.query.get(mentee_id)
                    mentor = Mentor.query.get(mentor_id)
                    
                    if mentee and mentor and not mentee.mentor_id:
                        if (mentee.subject in mentor.get_subjects_list() and 
                            mentor.can_take_more_mentees()):
                            mentee.mentor_id = int(mentor_id)
                            assigned_count += 1
                        else:
                            flash(f'Cannot assign {mentee.name} to {mentor.name}: incompatible or at capacity!', 'warning')
                
                db.session.commit()
                if assigned_count > 0:
                    flash(f'Successfully assigned {assigned_count} mentee(s)!', 'success')
                else:
                    flash('No mentees were assigned!', 'warning')
                    
            except Exception as e:
                db.session.rollback()
                flash(f'Error assigning mentees: {str(e)}', 'error')
        
        return redirect(url_for('bulk_assign_mentors'))
    
    # Get unassigned mentees and available mentors
    unassigned_mentees = Mentee.query.filter_by(mentor_id=None).all()
    mentors_list = Mentor.query.all()
    
    return render_template('bulk_assign_mentors.html', 
                         mentees=unassigned_mentees, 
                         mentors=mentors_list)

@app.route('/update_session_status', methods=['POST'])
def update_session_status():
    """Update the status of a session"""
    session_id = request.form.get('session_id')
    new_status = request.form.get('status')
    redirect_url = request.form.get('redirect_url', url_for('dashboard'))
    
    if not session_id or not new_status:
        flash('Invalid session update request!', 'error')
        return redirect(redirect_url)
    
    session = Session.query.get_or_404(session_id)
    old_status = session.status
    
    try:
        session.status = new_status
        
        # If marking as completed and was not completed before, reduce mentee's lessons
        if new_status == 'completed' and old_status != 'completed':
            if session.mentee.lessons_remaining > 0:
                session.mentee.lessons_remaining -= 1
        
        # If unmarking as completed and was completed before, increase mentee's lessons
        elif old_status == 'completed' and new_status != 'completed':
            session.mentee.lessons_remaining += 1
        
        db.session.commit()
        flash(f'Session status updated to {new_status}!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating session status: {str(e)}', 'error')
    
    return redirect(redirect_url)

@app.route('/bulk_delete_mentors', methods=['POST'])
def bulk_delete_mentors():
    """Bulk delete selected mentors"""
    selected_mentors = request.form.getlist('mentor_ids')
    
    if not selected_mentors:
        flash('No mentors selected for deletion!', 'error')
        return redirect(url_for('mentors'))
    
    try:
        deleted_count = 0
        for mentor_id in selected_mentors:
            mentor = Mentor.query.get(mentor_id)
            if mentor:
                # Unassign all mentees
                for mentee in mentor.mentees:
                    mentee.mentor_id = None
                
                # Delete associated sessions
                Session.query.filter_by(mentor_id=mentor_id).delete()
                
                # Delete mentor
                db.session.delete(mentor)
                deleted_count += 1
        
        db.session.commit()
        flash(f'Successfully deleted {deleted_count} mentor(s)!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting mentors: {str(e)}', 'error')
    
    return redirect(url_for('mentors'))

@app.route('/unassign_all_mentees/<int:mentor_id>', methods=['POST'])
def unassign_all_mentees(mentor_id):
    """Unassign all mentees from a specific mentor"""
    mentor = Mentor.query.get_or_404(mentor_id)
    
    try:
        # Get all mentees assigned to this mentor
        mentees = Mentee.query.filter_by(mentor_id=mentor_id).all()
        count = len(mentees)
        
        # Unassign all mentees
        for mentee in mentees:
            mentee.mentor_id = None
        
        db.session.commit()
        flash(f'Successfully unassigned {count} mentees from {mentor.name}!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error unassigning mentees: {str(e)}', 'error')
    
    return redirect(url_for('mentor_detail', id=mentor_id))

@app.route('/unassign_mentor/<int:id>', methods=['POST'])
def unassign_mentor(id):
    """Unassign mentor from a mentee"""
    mentee = Mentee.query.get_or_404(id)
    
    if mentee.mentor_id:
        old_mentor_name = mentee.assigned_mentor.name if mentee.assigned_mentor else "Unknown"
        mentee.mentor_id = None
        db.session.commit()
        flash(f'Mentor {old_mentor_name} unassigned from {mentee.name}!', 'success')
    else:
        flash(f'{mentee.name} has no assigned mentor!', 'warning')
    
    return redirect(url_for('mentee_detail', id=id))

# Template filters
@app.template_filter('datetime')
def datetime_filter(value, format='%Y-%m-%d %H:%M'):
    """Format datetime for templates"""
    if isinstance(value, str):
        return value
    return value.strftime(format) if value else ''

@app.template_filter('date')
def date_filter(value, format='%Y-%m-%d'):
    """Format date for templates"""
    if isinstance(value, str):
        return value
    return value.strftime(format) if value else ''

@app.template_filter('time')
def time_filter(value, format='%H:%M'):
    """Format time for templates"""
    if isinstance(value, str):
        return value
    return value.strftime(format) if value else ''

# Template context processors and filters
@app.template_global()
def moment():
    """Get current moment for template comparisons"""
    return datetime.now()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('base.html'), 500

# Initialize database
def init_db():
    """Initialize database tables"""
    with app.app_context():
        try:
            # Only create tables if they don't exist (don't drop existing data)
            db.create_all()
        except Exception as e:
            raise

if __name__ == '__main__':
    init_db()
    
    # Get configuration from environment variables
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Starting Mentorship System on {host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🔑 Secret key configured: {'✅' if app.config['SECRET_KEY'] != 'dev-key-change-in-production' else '⚠️  Using development key'}")
    
    app.run(debug=debug, host=host, port=port)

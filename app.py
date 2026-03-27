from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response, session
import sqlite3
import csv
from datetime import datetime
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = '68f1e1fb1e3e03c21d98d32d0ff500f3e46a716ec0b79f65ffefa2be59487738'

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comments TEXT,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            flash('Please login to access the admin dashboard', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        # Allowed admin emails
        allowed_emails = ['tharun120@admin.com', 'sudheer@admin.com']
        
        # Debug: Print login attempt (remove in production)
        print(f"Login attempt - Email: '{email}', Password: '{password}'")
        
        # Check if email is allowed and password is provided
        if email in allowed_emails and password:
            # Login successful (simplified authentication)
            session['user_logged_in'] = True
            session['user_email'] = email
            session['user_name'] = email.split('@')[0].title()  # Extract name from email
            session['is_admin'] = True
            
            print(f"Login successful for: {email}")
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            print(f"Login failed for: {email}")
            flash('Invalid email or password. Access restricted to authorized users only.', 'danger')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# Home page with feedback form
@app.route('/')
def index():
    return render_template('index.html')

# Submit feedback endpoint
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        rating = request.form.get('rating', '')
        comments = request.form.get('comments', '').strip()
        
        # Validation
        if not name or not email or not rating:
            return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400
        
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
        
        # Store in database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (name, email, rating, comments)
            VALUES (?, ?, ?, ?)
        ''', (name, email, rating, comments))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Feedback submitted successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred while submitting feedback'}), 500

# Admin dashboard
@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Get all feedback (first-come-first-serve - oldest first)
        cursor.execute('SELECT * FROM feedback ORDER BY date_submitted ASC')
        feedback_data = cursor.fetchall()
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) FROM feedback')
        total_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(rating) FROM feedback')
        avg_rating_result = cursor.fetchone()[0]
        avg_rating = round(avg_rating_result, 2) if avg_rating_result else 0
        
        cursor.execute('SELECT rating, COUNT(*) FROM feedback GROUP BY rating ORDER BY rating')
        rating_distribution = dict(cursor.fetchall())
        
        conn.close()
        
        # Format feedback data
        feedback_list = []
        for row in feedback_data:
            feedback_list.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'rating': row[3],
                'comments': row[4],
                'date_submitted': row[5]
            })
        
        return render_template('admin.html', 
                             feedback=feedback_list,
                             total_feedback=total_feedback,
                             avg_rating=avg_rating,
                             rating_distribution=rating_distribution)
        
    except Exception as e:
        flash('Error loading dashboard data')
        return render_template('admin.html', 
                             feedback=[],
                             total_feedback=0,
                             avg_rating=0,
                             rating_distribution={})

# Export data to CSV
@app.route('/export-csv')
def export_csv():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, email, rating, comments, date_submitted FROM feedback ORDER BY date_submitted DESC')
        
        def generate():
            data = cursor.fetchall()
            output = []
            output.append(['Name', 'Email', 'Rating', 'Comments', 'Date Submitted'])
            for row in data:
                output.append(list(row))
            
            # Convert to CSV string
            csv_string = ''
            for row in output:
                csv_string += ','.join(['"' + str(cell).replace('"', '""') + '"' for cell in row]) + '\n'
            
            return csv_string
        
        conn.close()
        
        return Response(
            generate(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=feedback_export.csv'}
        )
        
    except Exception as e:
        return jsonify({'error': 'Failed to export data'}), 500

# Delete feedback
@app.route('/delete-feedback/<int:feedback_id>', methods=['POST'])
@admin_required
def delete_feedback(feedback_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Check if feedback exists
        cursor.execute('SELECT id FROM feedback WHERE id = ?', (feedback_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Feedback not found'}), 404
        
        # Delete the feedback
        cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Feedback deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred while deleting feedback'}), 500

# Get chart data as JSON
@app.route('/chart-data')
def chart_data():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Rating distribution
        cursor.execute('SELECT rating, COUNT(*) FROM feedback GROUP BY rating ORDER BY rating')
        rating_data = dict(cursor.fetchall())
        
        # Daily feedback count for last 7 days
        cursor.execute('''
            SELECT DATE(date_submitted) as date, COUNT(*) as count
            FROM feedback
            WHERE date_submitted >= DATE('now', '-7 days')
            GROUP BY DATE(date_submitted)
            ORDER BY date
        ''')
        daily_data = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'rating_distribution': rating_data,
            'daily_feedback': daily_data
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to get chart data'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

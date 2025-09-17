from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Data for event categories
event_categories = [
    {"name": "Weddings", "image": "https://images.unsplash.com/photo-1597158292520-1683be8383c7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "base_price": 5000},
    {"name": "Engagements", "image": "https://images.unsplash.com/photo-1531905223429-6d8f35070d16?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "base_price": 2500},
    {"name": "Anniversaries", "image": "https://images.unsplash.com/photo-1529264232-237-835a61874c5a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "base_price": 1500},
    {"name": "Birthdays", "image": "https://images.unsplash.com/photo-1584592487924-c26902967a9e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "base_price": 1000},
    {"name": "Conferences", "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80", "base_price": 3000},
]

# Placeholder data for the user and their bookings
dummy_user = {
    "name": "Chetan Kumar",
    "email": "chetan.kumar@example.com",
    "age": 28,
    "address": "123 Tech Park, Bangalore, India",
    "profile_pic": "https://images.unsplash.com/photo-1557862921-37829c790f19?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80"
}

dummy_bookings = [
    {"event_name": "John & Jane's Wedding", "date": "2024-08-15", "status": "Past"},
    {"event_name": "Annual Tech Summit", "date": "2025-09-20", "status": "Future"},
    {"event_name": "Charity Gala", "date": "2025-11-01", "status": "Future"},
    {"event_name": "Marketing Seminar", "date": "2024-05-10", "status": "Past"},
    {"event_name": "New Year's Eve Party", "date": "2025-12-31", "status": "Pending"}
]

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Categorize bookings for display
    today = datetime.now().date()
    past_bookings = [b for b in dummy_bookings if b['status'] == 'Past']
    pending_bookings = [b for b in dummy_bookings if b['status'] == 'Pending']
    future_bookings = [b for b in dummy_bookings if b['status'] == 'Future']
    
    return render_template(
        'dashboard.html', 
        categories=event_categories, 
        user=dummy_user,
        past_bookings=past_bookings,
        pending_bookings=pending_bookings,
        future_bookings=future_bookings
    )

@app.route('/organize/<category_name>')
def organize(category_name):
    category = next((cat for cat in event_categories if cat['name'] == category_name), None)
    if category:
        return render_template('organize.html', category=category)
    return "Category not found", 404

if __name__ == '__main__':
    app.run(debug=True)
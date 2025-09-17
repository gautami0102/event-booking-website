from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Placeholder Data --- #

dummy_user = {
    "name": "Chetan",
    "profile_pic": "https://images.unsplash.com/photo-1557862921-37829c790f19?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80"
}

upcoming_bookings = [] # Empty for now to highlight other sections

recommended_events = {
    "Music & Concerts": [
        {"name": "Indie Rock Night", "date": "2025-11-20", "location": "The Underground", "price": "$25"}
    ]
}

booking_history = [
    {"name": "Rock On! Live", "date": "2024-08-10", "location": "Amphitheater", "review_pending": True}
]

wishlist_events = [] # Empty for now

wallet_data = {
    "balance": 150.75,
    "points": 2500,
    "promo_codes": [
        {"code": "SAVE20", "description": "Get 20% off on all music events"},
        {"code": "FIRSTBOOK", "description": "$10 off your first booking"}
    ]
}

# --- Routes --- #

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
    return render_template(
        'customer_dashboard.html', 
        user=dummy_user,
        upcoming_bookings=upcoming_bookings,
        recommended_events=recommended_events
    )

@app.route('/my-bookings')
def my_bookings():
    return render_template('my_bookings.html', user=dummy_user, bookings=booking_history)

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html', user=dummy_user, events=wishlist_events)

@app.route('/wallet')
def wallet():
    return render_template('wallet.html', user=dummy_user, wallet=wallet_data)

if __name__ == '__main__':
    app.run(debug=True)
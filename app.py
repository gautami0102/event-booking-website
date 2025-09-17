from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

app = Flask(__name__)

# --- Placeholder Data --- #

dummy_user = {
    "name": "Chetan",
    "profile_pic": "https://images.unsplash.com/photo-1557862921-37829c790f19?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80"
}

upcoming_bookings = [] # Empty for now to highlight other sections

recommended_events = {
    "Weddings & Personal Celebrations": [
        {"name": "Elegant Garden Wedding", "date": "2025-12-15", "location": "Rose Garden Venue", "price": "₹2,50,000", "image": "https://images.unsplash.com/photo-1519741497674-611481863552?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Beach Wedding Ceremony", "date": "2025-12-20", "location": "Sunset Beach Resort", "price": "₹3,20,000", "image": "https://images.unsplash.com/photo-1606800052052-a08af7148866?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Corporate Events": [
        {"name": "Annual Tech Conference", "date": "2025-11-25", "location": "Convention Center", "price": "₹15,000", "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Product Launch Event", "date": "2025-12-01", "location": "Grand Hotel Ballroom", "price": "₹20,000", "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Entertainment Events": [
        {"name": "Comedy Night Live", "date": "2025-11-18", "location": "Laugh Factory", "price": "₹3,500", "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Magic Show Spectacular", "date": "2025-12-05", "location": "Theater District", "price": "₹4,500", "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Sports Events": [
        {"name": "Marathon Run 2025", "date": "2025-11-30", "location": "Central Park", "price": "₹5,000", "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Basketball Championship", "date": "2025-12-10", "location": "Sports Arena", "price": "₹7,500", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Festivals & Cultural Events": [
        {"name": "Food & Wine Festival", "date": "2025-11-22", "location": "Downtown Plaza", "price": "₹8,000", "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Art & Culture Fair", "date": "2025-12-08", "location": "Museum District", "price": "₹2,500", "image": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Exhibitions & Trade Shows": [
        {"name": "Tech Innovation Expo", "date": "2025-11-28", "location": "Exhibition Center", "price": "₹10,000", "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Fashion Week Showcase", "date": "2025-12-12", "location": "Fashion District", "price": "₹12,000", "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Religious/Spiritual Events": [
        {"name": "Community Prayer Service", "date": "2025-11-24", "location": "Community Center", "price": "Free", "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Meditation Workshop", "date": "2025-12-03", "location": "Zen Garden", "price": "₹3,000", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Workshops & Educational Events": [
        {"name": "Digital Marketing Masterclass", "date": "2025-11-26", "location": "Business School", "price": "₹15,000", "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Photography Workshop", "date": "2025-12-07", "location": "Art Studio", "price": "₹9,000", "image": "https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Community & Social Gatherings": [
        {"name": "Neighborhood Block Party", "date": "2025-11-29", "location": "Main Street", "price": "Free", "image": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Charity Fundraiser Gala", "date": "2025-12-14", "location": "Grand Ballroom", "price": "₹20,000", "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Travel & Destination Events": [
        {"name": "Mountain Adventure Retreat", "date": "2025-12-18", "location": "Alpine Resort", "price": "₹50,000", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Beach Yoga Retreat", "date": "2025-12-22", "location": "Tropical Paradise", "price": "₹35,000", "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ],
    "Music & Concerts": [
        {"name": "Indie Rock Night", "date": "2025-11-20", "location": "The Underground", "price": "₹2,500", "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Jazz & Blues Evening", "date": "2025-12-06", "location": "Blue Note Club", "price": "₹4,000", "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
        {"name": "Electronic Music Festival", "date": "2025-12-16", "location": "Festival Grounds", "price": "₹8,000", "image": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"}
    ]
}

booking_history = [
    {"name": "Rock On! Live", "date": "2024-08-10", "location": "Amphitheater", "review_pending": True}
]

wishlist_events = [] # Empty for now

wallet_data = {
    "balance": 15075.00,
    "points": 2500,
    "promo_codes": [
        {"code": "SAVE20", "description": "Get 20% off on all music events"},
        {"code": "FIRSTBOOK", "description": "₹1,000 off your first booking"}
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

@app.route('/help')
def help_support():
    return render_template('help_support.html', user=dummy_user)

@app.route('/settings')
def settings():
    return render_template('settings.html', user=dummy_user)

@app.post('/api/chat')
def chat_api():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({"reply": "Please type a message."}), 400

    if not GENAI_AVAILABLE:
        return jsonify({"reply": "AI service is not available on the server."}), 503

    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({"reply": "Server missing GEMINI_API_KEY. Please set it and restart."}), 500

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message)
        text = getattr(response, 'text', None) or 'Sorry, no response.'
        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({"reply": f"Error from AI: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
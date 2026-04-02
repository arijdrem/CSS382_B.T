from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'studyspots.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Make int() available in Jinja2 templates
app.jinja_env.globals.update(int=int)

# Database Models
class StudySpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    noise_level = db.Column(db.String(20), nullable=False)  # quiet, moderate, loud
    outlets_available = db.Column(db.Boolean, default=False)
    wifi_quality = db.Column(db.Float, default=3.0)  # 1-5 rating
    vibe = db.Column(db.String(50), nullable=False)  # quiet study, group-friendly, cozy, outdoor
    address = db.Column(db.String(200), nullable=False)
    reviews = db.relationship('Review', backref='spot', lazy=True, cascade='all, delete-orphan')
    
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'noise_level': self.noise_level,
            'outlets_available': self.outlets_available,
            'wifi_quality': self.wifi_quality,
            'vibe': self.vibe,
            'address': self.address,
            'average_rating': self.average_rating(),
            'review_count': len(self.reviews)
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('study_spot.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review_text = db.Column(db.Text, nullable=False)
    student_name = db.Column(db.String(100), default='Anonymous')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables and add sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if StudySpot.query.first() is None:
            spots = [
                StudySpot(
                    name='UW Bothell Library',
                    description='Main library with quiet study areas, group study rooms, and computer labs. Multiple floors with different noise levels.',
                    noise_level='quiet',
                    outlets_available=True,
                    wifi_quality=4.8,
                    vibe='quiet study',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='ARC (Athletic and Recreation Center)',
                    description='Modern facility with flexible study areas, comfortable seating, and a great view. Good for focused study with some activity around.',
                    noise_level='moderate',
                    outlets_available=True,
                    wifi_quality=4.5,
                    vibe='group-friendly',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='UW2 Building',
                    description='Collaborative learning spaces with modern furniture, whiteboard walls, and break-out areas. Ideal for group projects.',
                    noise_level='moderate',
                    outlets_available=True,
                    wifi_quality=4.7,
                    vibe='group-friendly',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='UW1 Collaborative Spaces',
                    description='Open, flexible spaces designed for collaboration with plenty of seating options, natural light, and interactive surfaces.',
                    noise_level='moderate',
                    outlets_available=True,
                    wifi_quality=4.6,
                    vibe='group-friendly',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='Cafe Zingaro',
                    description='Cozy local coffee shop with excellent coffee, pastries, and a warm atmosphere. Perfect for casual study sessions.',
                    noise_level='moderate',
                    outlets_available=True,
                    wifi_quality=4.3,
                    vibe='cozy',
                    address='15100 Main St, Bothell, WA 98011'
                ),
                StudySpot(
                    name='Campus Green',
                    description='Beautiful outdoor space with benches and natural surroundings. Great for studying on nice days and getting fresh air.',
                    noise_level='moderate',
                    outlets_available=False,
                    wifi_quality=3.5,
                    vibe='outdoor',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='UWB Bookstore Lounge',
                    description='Quiet lounge area near the bookstore with comfortable seating and good lighting. Less crowded than main study areas.',
                    noise_level='quiet',
                    outlets_available=True,
                    wifi_quality=4.4,
                    vibe='quiet study',
                    address='18115 Campus Way NE, Bothell, WA 98011'
                ),
                StudySpot(
                    name='The Blend Coffee House',
                    description='Hip, modern coffee shop with strong WiFi, power outlets at most tables, and a studious crowd.',
                    noise_level='moderate',
                    outlets_available=True,
                    wifi_quality=4.6,
                    vibe='cozy',
                    address='15200 Main St, Bothell, WA 98011'
                ),
            ]
            db.session.add_all(spots)
            db.session.commit()
            
            # Add sample reviews
            reviews = [
                Review(spot_id=1, rating=5, review_text='Best place to study! Super quiet and resources are excellent.', student_name='Sarah M.'),
                Review(spot_id=1, rating=4, review_text='Great study spot, can get crowded during midterms.', student_name='Alex K.'),
                Review(spot_id=2, rating=5, review_text='Love the new facility! Great for group work.', student_name='Jordan L.'),
                Review(spot_id=5, rating=4, review_text='Amazing coffee and perfect atmosphere to study!', student_name='Casey P.'),
                Review(spot_id=6, rating=4, review_text='Beautiful outdoor space, perfect for sunny days!', student_name='Taylor R.'),
            ]
            db.session.add_all(reviews)
            db.session.commit()

# Routes
@app.route('/')
def index():
    noise_level = request.args.get('noise_level', '')
    outlets = request.args.get('outlets', '')
    vibe = request.args.get('vibe', '')
    
    query = StudySpot.query
    
    if noise_level:
        query = query.filter_by(noise_level=noise_level)
    if outlets == 'yes':
        query = query.filter_by(outlets_available=True)
    elif outlets == 'no':
        query = query.filter_by(outlets_available=False)
    if vibe:
        query = query.filter_by(vibe=vibe)
    
    spots = query.all()
    
    # Get unique values for filters
    all_spots = StudySpot.query.all()
    noise_levels = sorted(list(set([s.noise_level for s in all_spots])))
    vibes = sorted(list(set([s.vibe for s in all_spots])))
    
    return render_template('index.html', 
                         spots=spots,
                         noise_levels=noise_levels,
                         vibes=vibes,
                         selected_noise=noise_level,
                         selected_outlets=outlets,
                         selected_vibe=vibe)

@app.route('/spot/<int:spot_id>')
def spot_detail(spot_id):
    spot = StudySpot.query.get_or_404(spot_id)
    reviews = Review.query.filter_by(spot_id=spot_id).order_by(Review.created_at.desc()).all()
    return render_template('spot_detail.html', spot=spot, reviews=reviews)

@app.route('/spot/<int:spot_id>/review', methods=['GET', 'POST'])
def add_review(spot_id):
    spot = StudySpot.query.get_or_404(spot_id)
    
    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        review_text = request.form.get('review_text')
        student_name = request.form.get('student_name', 'Anonymous')
        
        if not rating or not review_text:
            return render_template('add_review.html', spot=spot, error='All fields are required!')
        
        if rating < 1 or rating > 5:
            return render_template('add_review.html', spot=spot, error='Rating must be between 1 and 5!')
        
        review = Review(
            spot_id=spot_id,
            rating=rating,
            review_text=review_text,
            student_name=student_name
        )
        db.session.add(review)
        db.session.commit()
        
        return redirect(url_for('spot_detail', spot_id=spot_id))
    
    return render_template('add_review.html', spot=spot)

@app.route('/api/spots')
def api_spots():
    spots = StudySpot.query.all()
    return jsonify([spot.to_dict() for spot in spots])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

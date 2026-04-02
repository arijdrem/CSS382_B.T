# CSS382_B.T - UW Bothell Study Spot Finder

## CSS 382 - Short AI Project

**NetID:** btanvir

**Name:** Boushra Tanvir

**GitHub Repository:** https://github.com/arijdrem/CSS382_B.T.git

**Deployed Site:** http://127.0.0.1:5000

### Idea

Create a web app that helps UW Bothell students find and rate study spots on and around campus. Users can browse locations, filter by features like noise level, outlet availability, and Wi-Fi quality, and leave ratings/reviews to help other students find their ideal study environment.

---

## Project Overview 📚

A Flask-based web application that enables UW Bothell students to discover, explore, and rate study locations across campus and nearby areas. The app helps students find the perfect study environment based on their needs and preferences.

## Features ✨

✅ **8 Pre-loaded Study Spots** including:
  - UW Bothell Library
  - ARC (Athletic and Recreation Center)
  - UW2 Building
  - UW1 Collaborative Spaces
  - Cafe Zingaro
  - Campus Green
  - UWB Bookstore Lounge
  - The Blend Coffee House

✅ **Comprehensive Spot Information**
  - Name, description, and address
  - Noise level (quiet/moderate/loud)
  - Power outlet availability
  - Wi-Fi quality rating (1-5)
  - Study vibe tags (quiet study, group-friendly, cozy, outdoor)
  - Average rating from community reviews

✅ **Advanced Filtering**
  - Filter by noise level
  - Filter by outlet availability
  - Filter by study vibe
  - Combine multiple filters

✅ **User Reviews System**
  - Leave star ratings (1-5 stars)
  - Write detailed reviews and tips
  - Optional student name or post anonymously
  - View all reviews with timestamps

✅ **Modern UI Design**
  - UW Bothell colors (Purple #3B0066 & Gold #FFB81C)
  - Fully responsive design (mobile, tablet, desktop)
  - Clean, intuitive interface

✅ **Persistent Data Storage**
  - SQLite database for reliability
  - Stores all spots and reviews permanently

## Tech Stack 🛠️

- **Backend:** Flask 2.3.3 (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, Jinja2 templating, CSS3
- **Libraries:** Flask-SQLAlchemy 3.0.5, SQLAlchemy 2.0.21

## Project Structure

```
CSS382_B.T/
├── app.py                    # Main Flask application & database models
├── requirements.txt          # Python dependencies
├── studyspots.db            # SQLite database (auto-generated)
├── README.md                # This file
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Home page & spots listing
│   ├── spot_detail.html     # Individual spot details & reviews
│   └── add_review.html      # Review submission form
└── static/                  # Static files
    └── style.css            # Main stylesheet (CSS)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- macOS/Linux/Windows terminal

### Step 1: Install Dependencies

Navigate to the project directory and install required packages:

```bash
cd /Users/student/Downloads/CSS382/CSS382_B.T
python3 -m pip install --user -r requirements.txt
```

**Note:** Use the `--user` flag on macOS to avoid permission issues.

### Step 2: Run the Application

Start the Flask development server:

```bash
python3 app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 3: Access the App

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage Guide 📖

### Home Page
- View all available study spots in a grid layout
- See quick information: noise level, outlets, Wi-Fi rating, vibe tag
- View average rating and review count for each spot

### Filtering
1. Scroll to the "Filter Study Spots" section
2. Select desired filters:
   - **Noise Level:** quiet, moderate, or loud
   - **Outlets:** Yes or No
   - **Vibe:** quiet study, group-friendly, cozy, or outdoor
3. Click "Filter" to apply
4. Click "Clear Filters" to see all spots again

### View Spot Details
1. Click "View Details & Reviews" on any spot card
2. See comprehensive information:
   - Full description and address
   - All amenities and quality ratings
   - Complete list of user reviews
   - Average rating from the community

### Leave a Review
1. On the spot detail page, click "✍️ Leave a Review"
2. Fill in the form:
   - **Your Name** (optional - defaults to "Anonymous")
   - **Rating** (select 1-5 stars)
   - **Review** (share your experience, max 500 characters)
3. Click "Submit Review"

## Database Schema

### StudySpot Table
```
- id (Integer, Primary Key)
- name (String)
- description (Text)
- noise_level (String: quiet/moderate/loud)
- outlets_available (Boolean)
- wifi_quality (Float: 1-5)
- vibe (String: quiet study/group-friendly/cozy/outdoor)
- address (String)
```

### Review Table
```
- id (Integer, Primary Key)
- spot_id (Integer, Foreign Key)
- rating (Integer: 1-5)
- review_text (Text, max 500 chars)
- student_name (String, default "Anonymous")
- created_at (DateTime, auto-timestamp)
```

## Troubleshooting 🔧

### Port 5000 Already in Use
```bash
lsof -ti:5000 | xargs kill -9
python3 app.py
```

### Permission Denied During Installation
Always use the `--user` flag with pip on macOS:
```bash
python3 -m pip install --user -r requirements.txt
```

### Database Reset
To reset the database (all spots and reviews will be deleted):
```bash
rm studyspots.db
python3 app.py
```

## Design & Styling 🎨

### Color Scheme
- **Primary:** UW Purple (#3B0066)
- **Accent:** UW Gold (#FFB81C)
- **Light Background:** #FAFAFA
- **Card Background:** White

### Responsive Breakpoints
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: < 768px

## Future Enhancements 🚀

Potential features to add:
- User authentication and accounts
- Photos/images of study spots
- Favorite/bookmark functionality
- Study spot hours of operation
- Map integration
- Social sharing
- Mobile app version

---

**Last Updated:** April 2, 2026
**Version:** 1.0
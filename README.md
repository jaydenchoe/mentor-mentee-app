# Mentor-Mentee Matching App

A web application for matching mentors and mentees built with Python Flask backend and React frontend.

## Features

- User registration and authentication with JWT
- Profile management with image upload
- Mentor discovery with filtering and sorting
- Match request system
- Role-based access control (mentor/mentee)

## Tech Stack

### Backend
- Python Flask
- SQLAlchemy (SQLite database)
- JWT Authentication
- Flask-CORS for cross-origin requests
- Swagger UI for API documentation

### Frontend
- React 18
- React Router for navigation
- Axios for HTTP requests
- Modern CSS with responsive design

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation & Setup

1. **Clone and navigate to the project directory:**
   ```bash
   cd mentor-mentee-app
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Application

### Start Backend Server (Terminal 1)
```bash
cd backend
# Activate virtual environment if not already active
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

python app.py
```
Backend will be available at: http://localhost:8080

### Start Frontend Server (Terminal 2)
```bash
cd frontend
npm start
```
Frontend will be available at: http://localhost:3000

## API Documentation

Once the backend is running, you can access:
- **Swagger UI:** http://localhost:8080/swagger-ui
- **OpenAPI Spec:** http://localhost:8080/api/openapi.json

## Usage

1. **Sign Up:** Create an account as either a mentor or mentee
2. **Login:** Authenticate with your credentials
3. **Complete Profile:** Add your bio, skills (for mentors), and profile image
4. **For Mentees:**
   - Browse mentors in the "Find Mentors" section
   - Filter by skills or sort by name/skills
   - Send match requests to mentors
   - View request status in "Requests" section
5. **For Mentors:**
   - View incoming requests in "Requests" section
   - Accept or reject requests (can only accept one at a time)
   - Update skills and profile information

## Database

The app uses SQLite database which will be automatically created as `mentor_mentee.db` in the backend directory when you first run the application.

## Security Features

- JWT token authentication with 1-hour expiration
- Password hashing using Werkzeug
- Input validation and sanitization
- SQL injection protection through SQLAlchemy ORM
- XSS protection through proper data handling
- Image validation (format, size, dimensions)

## Project Structure

```
mentor-mentee-app/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── mentor_mentee.db   # SQLite database (created on first run)
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js         # Main React app
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Styles
│   └── package.json       # Node.js dependencies
└── README.md
```

## Development Notes

- Backend runs on port 8080
- Frontend runs on port 3000  
- Frontend is configured to proxy API requests to backend
- Database is automatically initialized on first run
- Profile images are stored as binary data in the database
- Default profile images are served from placehold.co

## Troubleshooting

1. **Port conflicts:** Make sure ports 3000 and 8080 are available
2. **Virtual environment:** Ensure Python virtual environment is activated before running backend
3. **Dependencies:** Run `pip install -r requirements.txt` and `npm install` if packages are missing
4. **Database issues:** Delete `mentor_mentee.db` to reset the database (will lose all data)

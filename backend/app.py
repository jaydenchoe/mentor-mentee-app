from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import html
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
import os
import io
import base64
import jwt as pyjwt  # PyJWT를 별명으로 import
from PIL import Image
import bcrypt
import uuid
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentor_mentee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'mentor' or 'mentee'
    bio = db.Column(db.Text, default='')
    skills = db.Column(db.Text, default='')  # JSON string for mentor skills
    profile_image = db.Column(db.String(255))  # Store filename instead of binary data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MatchRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, default='')
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mentee = db.relationship('User', foreign_keys=[mentee_id], backref='sent_requests')
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='received_requests')

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def validate_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        width, height = image.size
        
        # Check if image is square and within size limits
        if width != height:
            return False, "Image must be square"
        if width < 500 or width > 1000:
            return False, "Image dimensions must be between 500x500 and 1000x1000 pixels"
        
        return True, None
    except Exception as e:
        return False, f"Invalid image: {str(e)}"

def create_jwt_token(user):
    """Create JWT token using Flask-JWT-Extended with RFC 7519 standard claims"""
    import time
    
    now = time.time()
    additional_claims = {
        # RFC 7519 standard claims
        'iss': 'mentor-mentee-app',  # Issuer
        'sub': str(user.id),         # Subject (user ID)
        'aud': 'mentor-mentee-users', # Audience
        'iat': int(now),             # Issued at
        'nbf': int(now),             # Not before
        'jti': str(uuid.uuid4()),    # JWT ID
        # Custom claims
        'name': user.name,
        'email': user.email,
        'role': user.role
    }
    
    return create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )

# API Routes
@app.route('/')
def index():
    return redirect('/swagger-ui')

@app.route('/api/auth/register', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        if data['role'] not in ['mentor', 'mentee']:
            return jsonify({'error': 'Role must be either mentor or mentee'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            name=data['name'],
            role=data['role']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return '', 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            token = create_jwt_token(user)
            return jsonify({
                'access_token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role
                }
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # 에러 상세 정보 출력
        import traceback
        traceback.print_exc()  # 전체 스택 트레이스 출력
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile_data = {
            'name': user.name,
            'bio': user.bio,
            'profile_image': user.profile_image
        }
        
        if user.role == 'mentor':
            skills = json.loads(user.skills) if user.skills else []
            profile_data['skills'] = skills
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'profile': profile_data
        })
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update basic profile info
        if 'name' in data:
            user.name = data['name']
        if 'bio' in data:
            user.bio = data['bio']
        
        # Update skills for mentors
        if user.role == 'mentor' and 'skills' in data:
            user.skills = json.dumps(data['skills'])
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(f"{user.id}_{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save and resize image
                try:
                    image = Image.open(file.stream)
                    image = image.resize((500, 500), Image.Resampling.LANCZOS)
                    image.save(file_path, optimize=True, quality=85)
                    
                    # Update user profile image filename
                    user.profile_image = filename
                except Exception as e:
                    return jsonify({'error': 'Failed to process image'}), 400
        
        db.session.commit()
        
        # Return updated profile
        profile_data = {
            'name': user.name,
            'bio': user.bio,
            'profile_image': user.profile_image
        }
        
        if user.role == 'mentor':
            import json
            skills = json.loads(user.skills) if user.skills else []
            profile_data['skills'] = skills
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'role': user.role,
            **profile_data
        })
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/users/<int:user_id>/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only upload their own profile images
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only JPG, JPEG, PNG allowed'}), 400
        
        # Generate unique filename
        filename = secure_filename(f"{user.id}_{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save and resize image
        try:
            image = Image.open(file.stream)
            image = image.resize((500, 500), Image.Resampling.LANCZOS)
            image.save(file_path, optimize=True, quality=85)
            
            # Remove old profile image if exists
            if user.profile_image:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Update user profile image filename
            user.profile_image = filename
            db.session.commit()
            
            return jsonify({'filename': filename, 'message': 'Image uploaded successfully'})
            
        except Exception as e:
            return jsonify({'error': 'Failed to process image'}), 400
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/mentors', methods=['GET'])
@jwt_required()
def get_mentors():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentee':
            return jsonify({'error': 'Only mentees can view mentors'}), 403
        
        query = User.query.filter_by(role='mentor')
        
        # Filter by skill if provided
        skill_filter = request.args.get('skill')
        if skill_filter:
            query = query.filter(User.skills.contains(f'"{skill_filter}"'))
        
        mentors = query.all()
        
        # Convert to list format
        mentor_list = []
        for mentor in mentors:
            skills = json.loads(mentor.skills) if mentor.skills else []
            
            mentor_list.append({
                'id': mentor.id,
                'name': mentor.name,
                'bio': mentor.bio,
                'skills': skills,
                'profile_image': mentor.profile_image
            })
        
        # Sort if requested
        order_by = request.args.get('orderBy')
        if order_by == 'name':
            mentor_list.sort(key=lambda x: x['name'])
        elif order_by == 'skill':
            mentor_list.sort(key=lambda x: ', '.join(x['skills']))
        
        return jsonify(mentor_list)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-requests', methods=['POST'])
@jwt_required()
def create_match_request():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentee':
            return jsonify({'error': 'Only mentees can send match requests'}), 403
        
        data = request.get_json()
        
        if 'mentorId' not in data:
            return jsonify({'error': 'Mentor ID required'}), 400
        
        mentor = User.query.get(data['mentorId'])
        if not mentor or mentor.role != 'mentor':
            return jsonify({'error': 'Mentor not found'}), 400
        
        # Check if mentee already has a pending request
        existing_request = MatchRequest.query.filter_by(
            mentee_id=current_user_id,
            status='pending'
        ).first()
        
        if existing_request:
            return jsonify({'error': 'You already have a pending match request'}), 400
        
        # Check if mentor already has an accepted match
        accepted_match = MatchRequest.query.filter_by(
            mentor_id=data['mentorId'],
            status='accepted'
        ).first()
        
        if accepted_match:
            return jsonify({'error': 'This mentor is already matched with another mentee'}), 400
        
        # Create new match request
        match_request = MatchRequest(
            mentee_id=current_user_id,
            mentor_id=data['mentorId'],
            message=data.get('message', ''),
            status='pending'
        )
        
        db.session.add(match_request)
        db.session.commit()
        
        return jsonify({
            'id': match_request.id,
            'mentorId': match_request.mentor_id,
            'message': match_request.message,
            'status': match_request.status,
            'createdAt': match_request.created_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-requests/incoming', methods=['GET'])
@jwt_required()
def get_incoming_match_requests():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentor':
            return jsonify({'error': 'Only mentors can view incoming requests'}), 403
        
        requests = MatchRequest.query.filter_by(mentor_id=current_user_id).all()
        
        request_list = []
        for req in requests:
            mentee = User.query.get(req.mentee_id)
            request_list.append({
                'id': req.id,
                'mentee': {
                    'id': mentee.id,
                    'name': mentee.name,
                    'bio': mentee.bio,
                    'profile_image': mentee.profile_image
                },
                'message': req.message,
                'status': req.status,
                'createdAt': req.created_at.isoformat()
            })
        
        return jsonify(request_list)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-requests/outgoing', methods=['GET'])
@jwt_required()
def get_outgoing_match_requests():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentee':
            return jsonify({'error': 'Only mentees can view outgoing requests'}), 403
        
        requests = MatchRequest.query.filter_by(mentee_id=current_user_id).all()
        
        request_list = []
        for req in requests:
            mentor = User.query.get(req.mentor_id)
            request_list.append({
                'id': req.id,
                'mentor': {
                    'id': mentor.id,
                    'name': mentor.name,
                    'bio': mentor.bio,
                    'profile_image': mentor.profile_image
                },
                'message': req.message,
                'status': req.status,
                'createdAt': req.created_at.isoformat()
            })
        
        return jsonify(request_list)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-requests/<int:request_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_match_request(request_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentor':
            return jsonify({'error': 'Only mentors can respond to requests'}), 403
        
        match_request = MatchRequest.query.get(request_id)
        if not match_request or match_request.mentor_id != current_user_id:
            return jsonify({'error': 'Match request not found'}), 404
        
        data = request.get_json()
        if 'action' not in data or data['action'] not in ['accept', 'reject']:
            return jsonify({'error': 'Action must be accept or reject'}), 400
        
        if data['action'] == 'accept':
            # Check if mentor already has an accepted match
            existing_accepted = MatchRequest.query.filter_by(
                mentor_id=current_user_id,
                status='accepted'
            ).first()
            
            if existing_accepted:
                return jsonify({'error': 'You already have an accepted match'}), 400
            
            match_request.status = 'accepted'
        else:
            match_request.status = 'rejected'
        
        match_request.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'id': match_request.id,
            'status': match_request.status,
            'updatedAt': match_request.updated_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/match-requests/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_match_request(request_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'mentee':
            return jsonify({'error': 'Only mentees can delete their requests'}), 403
        
        match_request = MatchRequest.query.get(request_id)
        if not match_request or match_request.mentee_id != current_user_id:
            return jsonify({'error': 'Match request not found'}), 404
        
        db.session.delete(match_request)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'bio': user.bio,
            'profile_image': user.profile_image,
            'created_at': user.created_at.isoformat()
        }
        
        if user.role == 'mentor':
            import json
            skills = json.loads(user.skills) if user.skills else []
            profile_data['skills'] = skills
        
        return jsonify(profile_data)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/users/<int:user_id>/profile', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only update their own profile
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update basic fields
        if 'name' in data:
            user.name = html.escape(data['name'])
        
        if 'bio' in data:
            user.bio = html.escape(data['bio'])
        
        # Update skills for mentors
        if user.role == 'mentor' and 'skills' in data:
            import json
            # Escape each skill
            escaped_skills = [html.escape(skill.strip()) for skill in data['skills'] if skill.strip()]
            user.skills = json.dumps(escaped_skills)
        
        db.session.commit()
        
        # Return updated profile
        profile_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'bio': user.bio,
            'profile_image': user.profile_image
        }
        
        if user.role == 'mentor':
            import json
            skills = json.loads(user.skills) if user.skills else []
            profile_data['skills'] = skills
        
        return jsonify(profile_data)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/demo-users', methods=['GET'])
def get_demo_users():
    """Get list of demo users for quick login"""
    try:
        demo_users = [
            # 멘토 2명 (대표)
            {
                'email': 'mentor1@example.com',
                'password': 'password123',
                'name': '최재훈',
                'role': 'mentor',
                'avatar': '👨‍💻',
                'description': '시니어 풀스택 개발자'
            },
            {
                'email': 'mentor2@example.com',
                'password': 'password123',
                'name': '김서연',
                'role': 'mentor',
                'avatar': '👩‍💼',
                'description': 'AI/ML 전문가'
            },
            # 멘티 2명 (대표)
            {
                'email': 'mentee1@example.com',
                'password': 'password123',
                'name': '최유민',
                'role': 'mentee',
                'avatar': '🧑‍🎓',
                'description': '컴공과 4학년'
            },
            {
                'email': 'mentee2@example.com',
                'password': 'password123',
                'name': '강다은',
                'role': 'mentee',
                'avatar': '👩‍🎓',
                'description': '비전공 신입개발자'
            }
        ]
        return jsonify(demo_users)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Swagger UI setup
@app.route('/api/openapi.json')
def openapi_spec():
    """Serve the OpenAPI specification"""
    try:
        # Simple OpenAPI spec without yaml dependency
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Mentor-Mentee Matching API",
                "version": "1.0.0",
                "description": "API for mentor-mentee matching platform"
            },
            "servers": [
                {"url": "http://localhost:8080", "description": "Development server"}
            ],
            "paths": {
                "/api/auth/register": {
                    "post": {
                        "summary": "Register a new user",
                        "tags": ["Authentication"],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "email": {"type": "string"},
                                            "password": {"type": "string"},
                                            "role": {"type": "string", "enum": ["mentor", "mentee"]}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/auth/login": {
                    "post": {
                        "summary": "Login user",
                        "tags": ["Authentication"]
                    }
                },
                "/api/mentors": {
                    "get": {
                        "summary": "Get list of mentors",
                        "tags": ["Mentors"]
                    }
                },
                "/api/match-requests": {
                    "post": {
                        "summary": "Create match request",
                        "tags": ["Matching"]
                    }
                }
            }
        }
        return jsonify(spec)
    except Exception as e:
        return jsonify({'error': f'OpenAPI spec error: {str(e)}'}), 404

SWAGGER_URL = '/swagger-ui'
API_URL = '/api/openapi.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mentor-Mentee Matching API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize database
def create_tables():
    db.create_all()

# Initialize demo users
def create_demo_users():
    """Create demo users if they don't exist"""
    demo_users = [
        # 멘토 5명
        {
            'email': 'mentor1@example.com',
            'password': 'password123',
            'name': '최재훈',  # 멘토 아이콘 로그인용
            'role': 'mentor',
            'bio': '시니어 풀스택 개발자로 10년 경력을 가지고 있습니다. React, Node.js, Python 전문가입니다.',
            'skills': ['React', 'Node.js', 'Python', 'AWS', 'Docker']
        },
        {
            'email': 'mentor2@example.com',
            'password': 'password123',
            'name': '김서연',
            'role': 'mentor',
            'bio': 'AI/ML 전문가로 대기업에서 데이터 사이언스 팀을 리드하고 있습니다.',
            'skills': ['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'Data Science']
        },
        {
            'email': 'mentor3@example.com',
            'password': 'password123',
            'name': '박민수',
            'role': 'mentor',
            'bio': '모바일 앱 개발 전문가로 iOS/Android 앱을 다수 런칭한 경험이 있습니다.',
            'skills': ['Swift', 'Kotlin', 'React Native', 'Flutter', 'Firebase']
        },
        {
            'email': 'mentor4@example.com',
            'password': 'password123',
            'name': '이지은',
            'role': 'mentor',
            'bio': 'DevOps 엔지니어로 클라우드 인프라 구축 및 자동화 전문가입니다.',
            'skills': ['AWS', 'Kubernetes', 'Terraform', 'Jenkins', 'Linux']
        },
        {
            'email': 'mentor5@example.com',
            'password': 'password123',
            'name': '정현우',
            'role': 'mentor',
            'bio': 'UI/UX 디자이너이자 프론트엔드 개발자로 사용자 경험 개선에 집중합니다.',
            'skills': ['Figma', 'React', 'TypeScript', 'CSS', 'UX Design']
        },
        # 멘티 5명
        {
            'email': 'mentee1@example.com',
            'password': 'password123',
            'name': '최유민',  # 멘티 아이콘 로그인용
            'role': 'mentee',
            'bio': '컴퓨터공학과 4학년으로 웹 개발에 관심이 많습니다. 졸업 후 프론트엔드 개발자가 되고 싶습니다.',
            'skills': ['HTML', 'CSS', 'JavaScript', 'React']
        },
        {
            'email': 'mentee2@example.com',
            'password': 'password123',
            'name': '강다은',
            'role': 'mentee',
            'bio': '비전공자로 국비지원 교육을 통해 개발을 배우고 있습니다. 백엔드 개발자를 목표로 하고 있습니다.',
            'skills': ['Python', 'Django', 'SQL']
        },
        {
            'email': 'mentee3@example.com',
            'password': 'password123',
            'name': '윤성민',
            'role': 'mentee',
            'bio': '부트캠프를 수료하고 첫 취업을 준비 중인 신입 개발자입니다.',
            'skills': ['JavaScript', 'Node.js', 'Express', 'MongoDB']
        },
        {
            'email': 'mentee4@example.com',
            'password': 'password123',
            'name': '손미영',
            'role': 'mentee',
            'bio': '데이터 분석에 관심이 있는 통계학과 학생입니다. 데이터 사이언티스트가 되고 싶습니다.',
            'skills': ['Python', 'Pandas', 'NumPy', 'R']
        },
        {
            'email': 'mentee5@example.com',
            'password': 'password123',
            'name': '조태현',
            'role': 'mentee',
            'bio': '모바일 앱 개발에 흥미를 느끼고 독학으로 공부하고 있는 대학생입니다.',
            'skills': ['Swift', 'Xcode', 'iOS']
        }
    ]
    
    for user_data in demo_users:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        if not existing_user:
            # Create new user
            user = User(
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                name=user_data['name'],
                role=user_data['role'],
                bio=user_data['bio'],
                skills=json.dumps(user_data['skills'])  # Store as JSON array
            )
            db.session.add(user)
    
    try:
        db.session.commit()
        print("데모 사용자들이 생성되었습니다.")
    except Exception as e:
        db.session.rollback()
        print(f"데모 사용자 생성 실패: {e}")

def migrate_skills_to_json():
    """Convert existing comma-separated skills to JSON format"""
    try:
        users = User.query.filter(User.skills != '').filter(User.skills != None).all()
        for user in users:
            if user.skills and not user.skills.startswith('['):
                # Convert comma-separated to JSON array
                skills_list = [skill.strip() for skill in user.skills.split(',') if skill.strip()]
                user.skills = json.dumps(skills_list)
        db.session.commit()
        print("스킬 데이터를 JSON 형태로 변환했습니다.")
    except Exception as e:
        db.session.rollback()
        print(f"스킬 데이터 변환 실패: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_demo_users()  # Create demo users on startup
        migrate_skills_to_json()  # Convert existing skills to JSON format
    app.run(host='0.0.0.0', port=8080, debug=True)

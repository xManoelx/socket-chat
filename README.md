# ChatApp - Real-Time Chat Application

A modern, full-featured chat application built with Flask and WebSocket technology that enables real-time communication across multiple chat rooms with user authentication and persistent message history.

## 🚀 Features

### Core Chat Functionality
- **Real-time Messaging**: Instant message delivery using WebSocket (Flask-SocketIO)
- **Multiple Chat Rooms**: Separate themed chat rooms (General, Programming, Games)
- **Message History**: Persistent message storage with timestamp tracking
- **Online User Tracking**: Real-time display of active users per room
- **Brazilian Time Zone**: Automatic conversion to Brazil timezone (UTC-3)

### User Management
- **User Authentication**: Secure login system with Flask-Login
- **Auto-Registration**: Automatic user creation for new usernames
- **Session Management**: Persistent login sessions across browser refreshes
- **Online Status**: Real-time online/offline status tracking
- **User Statistics**: Track user activity and last seen timestamps

### Room System
- **Dynamic Room Management**: Users can join/leave rooms dynamically
- **Room-specific Users**: Track which users are active in each room
- **Room Statistics**: Display user count and activity per room
- **Themed Rooms**: Pre-configured rooms for different topics

### Technical Features
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: Instant UI updates without page refresh
- **RESTful API**: JSON endpoints for user and room data
- **Database Integration**: SQLite with SQLAlchemy ORM
- **Error Handling**: Comprehensive validation and error responses

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **Real-time**: Flask-SocketIO for WebSocket communication
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Frontend**: HTML5, CSS3, JavaScript with Socket.IO client
- **Architecture**: MVC pattern with separate models and views

## 📋 Prerequisites

- Python 3.7 or higher
- Modern web browser with WebSocket support
- Basic understanding of chat applications

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatapp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-socketio
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

## 🚦 Running the Application

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Homepage: `http://127.0.0.1:5000`
   - Login: `http://127.0.0.1:5000/login`
   - Chat Rooms: `http://127.0.0.1:5000/rooms`

## 📚 Application Structure

### Routes Overview

#### Public Routes
- `GET /` - Landing page
- `GET /about` - Application information
- `GET/POST /login` - User authentication

#### Authenticated Routes
- `GET /homepage` - User dashboard with room selection
- `GET /rooms` - Room management interface
- `GET /chat/<room>` - Individual chat room interface
- `GET /logout` - User logout

#### API Endpoints
- `GET /api/users` - List all online users and room statistics
- `GET /api/users/<room>` - List users in specific room

### WebSocket Events

#### Client → Server Events
```javascript
// User status management
socket.emit('user_online', {username: 'username'});
socket.emit('user_offline', {username: 'username'});

// Room management  
socket.emit('join_room', {username: 'username', room: 'room_name'});
socket.emit('leave_room', {username: 'username', room: 'room_name'});

// Messaging
socket.emit('message', {
    username: 'username',
    message: 'message_content',
    room: 'room_name'
});
```

#### Server → Client Events
```javascript
// User notifications
socket.on('user_joined', function(data) {
    // Handle user joining room
});

socket.on('user_left', function(data) {
    // Handle user leaving room
});

// Message handling
socket.on('message', function(data) {
    // Display new message
});

// Statistics updates
socket.on('users_updated', function(data) {
    // Update user counts and lists
});
```

## 🗄️ Database Schema

### User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Room Model
```python
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Message Model
```python
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
```

### UserRoom Model (Junction Table)
```python
class UserRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## 🏗️ Project Architecture

```
chatapp/
├── app.py                 # Main Flask application with routes
├── models.py              # Database models and schema
├── init_db.py             # Database initialization script
├── templates/
│   └── pages/
│       ├── index.html     # Landing page
│       ├── login.html     # Authentication page
│       ├── homepage.html  # User dashboard
│       ├── rooms.html     # Room management
│       ├── chat.html      # Chat interface
│       └── about.html     # Application info
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── img/              # Images and assets
└── chatapp.db            # SQLite database
```

## 💬 Chat Flow Explained

### 1. User Authentication
```python
# User enters username
# System checks if user exists
# If new: create user account
# If existing: login existing user
# Set online status and redirect to homepage
```

### 2. Room Selection
```python
# User sees available rooms with live user counts
# Clicks "Entrar" to join specific room
# System adds user to room and updates counts
# User is redirected to chat interface
```

### 3. Real-time Messaging
```python
# User types message and sends
# WebSocket emits message to all users in room
# Message is saved to database with timestamp
# All connected users see message instantly
```

### 4. User Management
```python
# System tracks user online status
# Updates user counts in real-time
# Handles disconnections gracefully
# Maintains persistent chat history
```

## 🎨 UI/UX Features

### Responsive Design
- Mobile-friendly interface
- Adaptive layouts for different screen sizes
- Touch-friendly controls

### Real-time Feedback
- Instant message delivery
- Live user count updates  
- Visual indicators for online status
- Typing indicators (ready for implementation)

### Brazilian Localization
- Portuguese language interface
- Brazilian timezone (UTC-3) for timestamps
- Localized date/time formatting

## 🧪 Testing

### Manual Testing
```bash
# Test user registration/login
curl -X POST http://127.0.0.1:5000/login \
  -d "username=testuser" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Test API endpoints
curl http://127.0.0.1:5000/api/users
curl http://127.0.0.1:5000/api/users/geral
```

### WebSocket Testing
```javascript
// Connect to WebSocket
const socket = io('http://127.0.0.1:5000');

// Test room joining
socket.emit('join_room', {username: 'test', room: 'geral'});

// Test messaging
socket.emit('message', {
    username: 'test',
    message: 'Hello world!',
    room: 'geral'
});
```

## ⚙️ Configuration

### Default Rooms
The application comes with three pre-configured rooms:

1. **Chat Geral** (`geral`) - General conversation
2. **Programação** (`programacao`) - Programming discussions  
3. **Games** (`games`) - Gaming chat

### Environment Configuration
```python
app.config['SECRET_KEY'] = 'SECRET_KEY'  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## 🚀 Deployment Considerations

### Production Setup
1. **Change Secret Key**: Use environment variables
2. **Database**: Consider PostgreSQL for production
3. **HTTPS**: Enable SSL/TLS for security
4. **CORS**: Configure appropriate CORS policies
5. **Scaling**: Consider Redis for session storage

### Performance Optimization
- **Message Limits**: Implement message history pagination
- **User Limits**: Set maximum users per room
- **Rate Limiting**: Prevent message spam
- **Caching**: Cache user counts and room data

## 🔮 Future Enhancements

- [ ] **Private Messaging**: Direct user-to-user chat
- [ ] **File Sharing**: Image and document uploads
- [ ] **Emoji Support**: Rich text messaging with emojis
- [ ] **Typing Indicators**: Show when users are typing
- [ ] **Message Reactions**: Like/react to messages
- [ ] **Admin Panel**: Moderation tools and user management
- [ ] **Push Notifications**: Browser notifications for messages
- [ ] **Voice/Video**: WebRTC integration for calls
- [ ] **Mobile App**: React Native companion app
- [ ] **Message Search**: Full-text search in chat history

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check existing GitHub issues
- Create new issue with detailed information
- Include browser console logs for WebSocket issues
- Provide steps to reproduce any bugs

## 🏆 Acknowledgments

- Flask and Flask-SocketIO communities
- Socket.IO documentation and examples
- Modern web chat application best practices

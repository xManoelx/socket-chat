from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Classe de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com mensagens
    messages = db.relationship('Message', backref='author', lazy=True)

    # Representação do usuário
    def __repr__(self):
        return f'<User {self.username}>'

# Classe de Sala
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com mensagens
    messages = db.relationship('Message', backref='room', lazy=True)

    # Relacionamento com usuários
    def __repr__(self):
        return f'<Room {self.name}>'

# Classe de Mensagem
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Representação da mensagem
    def __repr__(self):
        return f'<Message {self.id}>'

    # Representação da mensagem em formato de dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%H:%M'),
            'username': self.author.username,
            'room': self.room.name
        }

# Classe de Usuário em Sala
class UserRoom(db.Model):
    """Tabela de relacionamento para usuários online por sala"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='user_rooms')
    room_obj = db.relationship('Room', backref='room_users')
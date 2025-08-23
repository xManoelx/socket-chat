from flask import request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from models import db, User
from datetime import datetime

# Função para autenticar ou criar usuário
def authenticate_user(username):
    if not username or len(username.strip()) < 2:
        return False, "Nome de usuário deve ter pelo menos 2 caracteres"
    
    username = username.strip()
    
    # Verificar se o usuário já existe
    user = User.query.filter_by(username=username).first()
    
    # Usuário existe, fazer login
    if user:    
        user.is_online = True
        user.last_seen = datetime.utcnow()
    
    # Criar novo usuário
    else:
        user = User(username=username, is_online=True)
        db.session.add(user)
    
    try:
        db.session.commit()
        login_user(user)
        session['username'] = username
        return True, "Login realizado com sucesso"
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao fazer login: {str(e)}"

# Função para deslogar usuário
def logout_current_user():

    # Verifica se o usuário está autenticado
    if current_user.is_authenticated:
        current_user.is_online = False
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        logout_user()
        session.pop('username', None)

# Função para obter lista de usuários online
def get_online_users():
    return User.query.filter_by(is_online=True).all()

# Função para obter usuários em uma sala específica
def get_users_in_room(room_name):
    from models import Room, UserRoom
    
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        return []
    
    user_rooms = UserRoom.query.filter_by(room_id=room.id).all()
    users = [ur.user for ur in user_rooms if ur.user.is_online]
    return users

# Função para adicionar usuário a uma sala
def user_join_room(username, room_name):
    from models import Room, UserRoom
    
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(name=room_name).first()
    
    if not user or not room:
        return False
    
    # Verificar se já está na sala
    existing = UserRoom.query.filter_by(user_id=user.id, room_id=room.id).first()
    if existing:
        return True
    
    # Adicionar à sala
    user_room = UserRoom(user_id=user.id, room_id=room.id)
    db.session.add(user_room)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# Função para remover usuário de uma sala
def user_leave_room(username, room_name):
    from models import Room, UserRoom
    
    user = User.query.filter_by(username=username).first()
    room = Room.query.filter_by(name=room_name).first()
    
    if not user or not room:
        return False
    
    user_room = UserRoom.query.filter_by(user_id=user.id, room_id=room.id).first()
    if user_room:
        db.session.delete(user_room)
        db.session.commit()
    
    return True
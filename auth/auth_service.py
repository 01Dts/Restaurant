from flask_jwt_extended import create_access_token

USERS = {
    'admin': 'admin123',
    'user1': 'password123',
    'test': 'test123'
}

def authenticate_user(username, password):
    """Validate credentials"""
    if username in USERS and USERS[username] == password:
        return create_access_token(identity=username)
    return None

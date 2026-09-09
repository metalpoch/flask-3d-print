from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

supabase: Client = create_client(
    os.environ.get('SUPABASE_URL', ''),
    os.environ.get('SUPABASE_KEY', '')
)


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_id(user_id):
        resp = supabase.table('users').select('*').eq('id', user_id).execute()
        if resp.data:
            u = resp.data[0]
            return User(u['id'], u['username'], u['password_hash'])
        return None

    @staticmethod
    def get_by_username(username):
        resp = supabase.table('users').select('*').eq('username', username).execute()
        if resp.data:
            u = resp.data[0]
            return User(u['id'], u['username'], u['password_hash'])
        return None

    @staticmethod
    def create(username, password):
        password_hash = generate_password_hash(password)
        resp = supabase.table('users').insert({
            'username': username,
            'password_hash': password_hash
        }).execute()
        if resp.data:
            u = resp.data[0]
            return User(u['id'], u['username'], u['password_hash'])
        return None

    @staticmethod
    def exists(username):
        resp = supabase.table('users').select('id').eq('username', username).execute()
        return len(resp.data) > 0

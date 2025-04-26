from sqlalchemy.orm import Session
from src.auth.auth_exception import UserNotFoundException
from src.auth.models.user import User  # Asegúrate de que el modelo exista

import hashlib


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: dict, show_password=False):
        hashed_password = self._encrypt_password(user_data["password"])
        new_user = User(
            username=user_data["username"],
            password=hashed_password,
            email=user_data.get("email")  # o los campos que uses
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        if not show_password:
            new_user.password = None
        return new_user

    def get_user_by(self, field: str, value: str, show_password=False):
        user = self.db.query(User).filter(getattr(User, field) == value).first()
        if user is None:
            raise UserNotFoundException("Usuario no encontrado")
        if not show_password:
            user.password = None
        return user

    def is_valid_user(self, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        if not user:
            return False
        return self.compare_password(user.password, password)

    @staticmethod
    def _encrypt_password(password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @staticmethod
    def compare_password(hashed, plain):
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

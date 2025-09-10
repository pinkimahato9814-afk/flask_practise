from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Users(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(80), nullable=False)
    profile = relationship("Profiles", back_populates="user", uselist=False)

class Profiles(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    age: Mapped[int] = mapped_column(db.Integer, nullable=False)
    amount: Mapped[float] = mapped_column(db.Float, nullable=False, default=0.0)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="profile")
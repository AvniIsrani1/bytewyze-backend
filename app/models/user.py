import secrets
import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlmodel import Field, SQLModel


def new_user_id() -> str:
    return str(uuid.uuid4())


def generate_username() -> str:
    # placeholder until the user picks their own, e.g. user_a3f9c2d1
    return f"user_{secrets.token_hex(4)}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    """Who the user is and how they sign in. Cooking data (equipment, methods, ...) gets its own tables."""

    __tablename__ = "users"

    # UUID stored as text (36 chars), matches the String id in the Flutter User model
    id: str = Field(default_factory=new_user_id, primary_key=True, max_length=36)

    # sign-in: email is always required, password_hash is empty for Google-only accounts
    email: str = Field(max_length=255, unique=True, index=True)
    email_verified: bool = Field(default=False)
    password_hash: str | None = Field(default=None, max_length=255)
    google_uid: str | None = Field(default=None, max_length=128, unique=True, index=True)

    # profile
    username: str = Field(default_factory=generate_username, max_length=50, unique=True, index=True)
    first_name: str = Field(max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)

    # app
    role: str = Field(default="user", max_length=20)
    points: int = Field(default=0)
    # stored as UTC
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )

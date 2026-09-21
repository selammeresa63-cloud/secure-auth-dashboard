import os

uri = os.environ.get("DATABASE_URL", "sqlite:///app.db")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri

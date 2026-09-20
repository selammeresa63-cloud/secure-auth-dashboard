from datetime import datetime, timezone
import pyotp
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=True)
    is_2fa_enabled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_totp(self, code):
        if not self.totp_secret:
            return False
        # valid_window=1: ±30 ሰከንድ የሰዓት ልዩነት ይፈቅዳል
        return pyotp.TOTP(self.totp_secret).verify(code, valid_window=1)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

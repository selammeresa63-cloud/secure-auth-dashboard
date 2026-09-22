# Secure Auth Dashboard

A Flask web application with secure user authentication: registration, login, and TOTP-based two-factor authentication (2FA), built with security best practices in mind.

**Live demo:** YOUR-LIVE-LINK *(Free hosting: the first load may take ~1 minute, and demo data is reset on restart.)*

## Features

- User registration and login with a responsive dashboard
- TOTP two-factor authentication (Google Authenticator, Aegis, etc.) with QR-code setup
- 2FA is only enabled after the user proves the first code works
- Password and code required to disable 2FA

## Architecture

```text
secure-auth-dashboard/
├── app/
│   ├── __init__.py      # App factory, extension init (SQLAlchemy, Login, Limiter, CSRF)
│   ├── models.py        # User model (password hash, TOTP secret, 2FA state)
│   ├── routes/
│   │   ├── auth.py      # Register, login, logout
│   │   └── twofa.py     # 2FA setup, verify, disable
│   ├── forms.py         # WTForms with server-side validation
│   └── templates/       # Jinja2 templates (auto-escaped)
├── config.py            # Environment-driven config (SQLite / PostgreSQL)
├── requirements.txt
├── run.py               # Entry point (dev server)
└── setup.sh             # One-command environment setup

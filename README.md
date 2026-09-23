# Secure Auth Dashboard (2FA Enabled)

A modern, monolithic Web Dashboard built with **Flask**, featuring **Two-Factor Authentication (TOTP)**, session fixation protection, and rate limiting.

## 🔑 Key Features

- **Two-Factor Authentication (TOTP):** QR-code based 2FA setup compatible with Google Authenticator and Authy using `pyotp`.
- **Security Hardening:** Rate limiting via `Flask-Limiter` to protect against brute-force attacks.
- **Session Security:** Session fixation mitigation during authentication and state changes.
- **Clean UI:** Responsive dashboard interface using standard CSS/HTML templates.

## 🛠️ Tech Stack

- **Framework:** Python, Flask
- **Security:** PyOTP, Flask-Login, Flask-Limiter
- **Database:** SQLite (SQLAlchemy)

## 🚀 How to Run Locally

```bash
git clone [https://github.com/selammeresa63-cloud/secure-auth-dashboard.git](https://github.com/selammeresa63-cloud/secure-auth-dashboard.git)
cd secure-auth-dashboard

# Set up Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run Application
flask run --port=5001

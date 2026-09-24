# SecureAuth - Flask Authentication & 2FA Dashboard

SecureAuth is a production-ready, monolithic web application designed with a strong focus on identity management and application security. Built using Python and Flask, it features robust authentication workflows, Time-based One-Time Password (TOTP) Multi-Factor Authentication (MFA), and proactive defensive protection mechanisms.

---

## Key Features

- **Robust User Authentication**: Secure registration and login workflows with password hashing.
- **Two-Factor Authentication (2FA)**: TOTP implementation using `PyOTP`, complete with dynamically generated QR codes for authenticator apps (Google Authenticator, Microsoft Authenticator, Aegis).
- **Session & State Management**: Secure session handling to mitigate session fixation attacks.
- **Rate Limiting & Defensive Controls**: Configured with `Flask-Limiter` to prevent brute-force login attempts.
- **Clean UI/UX**: Dark-themed, responsive user interface designed with modern web aesthetics.

---

## Architecture & Workflows

1. **User Registration & Login**: Users register with unique credentials and log in securely.
2. **MFA Enrolment**: Users can enable 2FA directly from their account dashboard by scanning an inline QR code.
3. **MFA Verification & Management**: Verification of 6-digit TOTP tokens with the ability to disable 2FA securely via re-authentication.

---

## Tech Stack

- **Backend Framework**: Python 3, Flask
- **Security & Cryptography**: PyOTP, Flask-Limiter, Werkzeug Security
- **Database**: SQLite / SQLAlchemy ORM
- **Frontend**: HTML5, Modern CSS3 (Dark Mode UX)

---

## Local Development Setup

```bash
# 1. Clone the repository
git clone [https://github.com/selammeresa63-cloud/secure-auth-dashboard.git](https://github.com/selammeresa63-cloud/secure-auth-dashboard.git)
cd secure-auth-dashboard

# 2. Set up and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
flask run --port=5001

import base64
import io
import time
import pyotp
import qrcode
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from app import db, limiter
from app.forms import DisableTOTPForm, LoginForm, RegisterForm, TOTPForm
from app.models import User

bp = Blueprint("main", __name__)

PRE_2FA_TTL = 300  # የይለፍ ቃል ከገባ በኋላ ኮድ ለማስገባት 5 ደቂቃ
MAX_2FA_TRIES = 5


def is_safe_next(target):
    """Allow only same-site relative paths (prevents open redirect)."""
    return (
        bool(target)
        and target.startswith("/")
        and not target.startswith("//")
        and "\\" not in target
    )


def qr_data_uri(text):
    img = qrcode.make(text)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


@bp.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            next_page = request.args.get("next")
            if not is_safe_next(next_page):
                next_page = None
            session.clear()  # session fixation መከላከያ
            if user.is_2fa_enabled:
                # ገና login አይደለም፤ የኮድ እርምጃ ይቀራል
                session["pre_2fa_uid"] = user.id
                session["pre_2fa_ts"] = time.time()
                session["pre_2fa_next"] = next_page
                session["pre_2fa_tries"] = 0
                return redirect(url_for("main.login_2fa"))
            login_user(user)
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@bp.route("/login/2fa", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login_2fa():
    uid = session.get("pre_2fa_uid")
    ts = session.get("pre_2fa_ts", 0)
    user = db.session.get(User, uid) if uid else None
    if not user or time.time() - ts > PRE_2FA_TTL:
        session.clear()
        flash("Session expired. Please log in again.", "info")
        return redirect(url_for("main.login"))
    form = TOTPForm()
    if form.validate_on_submit():
        tries = session.get("pre_2fa_tries", 0) + 1
        session["pre_2fa_tries"] = tries
        if user.verify_totp(form.code.data):
            next_page = session.get("pre_2fa_next")
            session.clear()
            login_user(user)
            return redirect(next_page or url_for("main.dashboard"))
        if tries >= MAX_2FA_TRIES:
            session.clear()
            flash("Too many wrong codes. Please log in again.", "danger")
            return redirect(url_for("main.login"))
        flash("Invalid code.", "danger")
    return render_template("login_2fa.html", form=form)


@bp.route("/2fa/setup", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute", methods=["POST"])
def setup_2fa():
    if current_user.is_2fa_enabled:
        flash("2FA is already enabled.", "info")
        return redirect(url_for("main.dashboard"))
    # secret ይፈጠራል ግን የመጀመሪያው ኮድ እስኪረጋገጥ ድረስ 2FA አይነቃም
    if not current_user.totp_secret:
        current_user.totp_secret = pyotp.random_base32()
        db.session.commit()
    form = TOTPForm()
    if form.validate_on_submit():
        if current_user.verify_totp(form.code.data):
            current_user.is_2fa_enabled = True
            db.session.commit()
            flash("Two-factor authentication is now enabled.", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid code. Try again.", "danger")
    uri = pyotp.TOTP(current_user.totp_secret).provisioning_uri(
        name=current_user.email, issuer_name="SecureAuth"
    )
    return render_template(
        "setup_2fa.html",
        form=form,
        qr=qr_data_uri(uri),
        secret=current_user.totp_secret,
    )


@bp.route("/2fa/disable", methods=["GET", "POST"])
@login_required
@limiter.limit("5 per minute", methods=["POST"])
def disable_2fa():
    if not current_user.is_2fa_enabled:
        return redirect(url_for("main.dashboard"))
    form = DisableTOTPForm()
    if form.validate_on_submit():
        if current_user.check_password(
            form.password.data
        ) and current_user.verify_totp(form.code.data):
            current_user.is_2fa_enabled = False
            current_user.totp_secret = None
            db.session.commit()
            flash("Two-factor authentication disabled.", "info")
            return redirect(url_for("main.dashboard"))
        flash("Invalid password or code.", "danger")
    return render_template("disable_2fa.html", form=form)


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))

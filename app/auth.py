from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        role = request.form.get("role", "staff").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not username or not password:
            flash("All fields are required.", "danger")
        elif User.query.filter_by(username=username).first():
            flash("Username is already registered.", "danger")
        elif role not in {"mayor", "staff"}:
            flash("Invalid role selection.", "danger")
        else:
            user = User(full_name=full_name, username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration completed. Please login.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Welcome to Hosana City Housing System.", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

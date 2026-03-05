import csv
from io import StringIO

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import HouseHolder


main_bp = Blueprint("main", __name__)
MENDERS = ["Mender 1", "Mender 2", "Mender 3"]
KEBELES = [f"Kebele {i}" for i in range(1, 11)]


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    q = request.args.get("q", "").strip()
    holders = HouseHolder.query
    if q:
        search = f"%{q}%"
        holders = holders.filter(
            db.or_(
                HouseHolder.house_number.ilike(search),
                HouseHolder.first_name.ilike(search),
                HouseHolder.last_name.ilike(search),
            )
        )
    holders = holders.order_by(HouseHolder.house_number.asc()).all()
    return render_template("dashboard.html", holders=holders, query=q)


@main_bp.route("/householders/new", methods=["GET", "POST"])
@login_required
def add_householder():
    if request.method == "POST":
        house_number = request.form.get("house_number", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone = request.form.get("phone", "").strip()
        mender = request.form.get("mender", "").strip()
        kebele = request.form.get("kebele", "").strip()
        family_size = request.form.get("family_size", "1").strip()
        notes = request.form.get("notes", "").strip()

        if not house_number or not first_name or not last_name:
            flash("House number and names are required.", "danger")
        elif mender not in MENDERS or kebele not in KEBELES:
            flash("Please choose a valid mender and kebele.", "danger")
        elif HouseHolder.query.filter_by(house_number=house_number).first():
            flash("House number already exists.", "danger")
        else:
            holder = HouseHolder(
                house_number=house_number,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                mender=mender,
                kebele=kebele,
                family_size=int(family_size) if family_size.isdigit() else 1,
                notes=notes,
            )
            db.session.add(holder)
            db.session.commit()
            flash("Householder profile created.", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("householder_form.html", holder=None, menders=MENDERS, kebeles=KEBELES)


@main_bp.route("/householders/<int:holder_id>/edit", methods=["GET", "POST"])
@login_required
def edit_householder(holder_id: int):
    holder = HouseHolder.query.get_or_404(holder_id)

    if request.method == "POST":
        house_number = request.form.get("house_number", "").strip()
        if house_number != holder.house_number and HouseHolder.query.filter_by(house_number=house_number).first():
            flash("House number already exists.", "danger")
            return render_template("householder_form.html", holder=holder, menders=MENDERS, kebeles=KEBELES)

        holder.house_number = house_number
        holder.first_name = request.form.get("first_name", "").strip()
        holder.last_name = request.form.get("last_name", "").strip()
        holder.phone = request.form.get("phone", "").strip()
        holder.mender = request.form.get("mender", "").strip()
        holder.kebele = request.form.get("kebele", "").strip()

        family_size = request.form.get("family_size", "1").strip()
        holder.family_size = int(family_size) if family_size.isdigit() else 1
        holder.notes = request.form.get("notes", "").strip()

        if holder.mender not in MENDERS or holder.kebele not in KEBELES or not holder.house_number:
            flash("Please complete valid required fields.", "danger")
            return render_template("householder_form.html", holder=holder, menders=MENDERS, kebeles=KEBELES)

        db.session.commit()
        flash("Householder profile updated.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("householder_form.html", holder=holder, menders=MENDERS, kebeles=KEBELES)


@main_bp.route("/householders/upload", methods=["POST"])
@login_required
def upload_householders():
    upload = request.files.get("file")
    if not upload or not upload.filename.endswith(".csv"):
        flash("Please upload a CSV file.", "danger")
        return redirect(url_for("main.dashboard"))

    content = upload.stream.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))
    created = 0

    for row in reader:
        house_number = row.get("house_number", "").strip()
        first_name = row.get("first_name", "").strip()
        last_name = row.get("last_name", "").strip()
        mender = row.get("mender", "").strip()
        kebele = row.get("kebele", "").strip()

        if not house_number or not first_name or not last_name:
            continue
        if mender not in MENDERS or kebele not in KEBELES:
            continue
        if HouseHolder.query.filter_by(house_number=house_number).first():
            continue

        holder = HouseHolder(
            house_number=house_number,
            first_name=first_name,
            last_name=last_name,
            phone=row.get("phone", "").strip(),
            mender=mender,
            kebele=kebele,
            family_size=int(row.get("family_size", 1)) if str(row.get("family_size", "")).isdigit() else 1,
            notes=row.get("notes", "").strip(),
        )
        db.session.add(holder)
        created += 1

    db.session.commit()
    flash(f"Upload completed. Added {created} householder records.", "success")
    return redirect(url_for("main.dashboard"))

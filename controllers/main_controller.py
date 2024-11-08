from flask import Blueprint, render_template, url_for, redirect, session

main_controller = Blueprint("main_controller", __name__)

@main_controller.route("/")
def index():
    if "username" in session:
        return redirect(url_for('dashboard_controller.dashboard'))
    return render_template("index.html")
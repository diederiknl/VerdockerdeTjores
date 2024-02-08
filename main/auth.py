from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database_functions import *
from werkzeug.security import check_password_hash


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        connection = get_db()
        cursor = connection.cursor()
        name = request.form['name']
        password = request.form['password']
        query = "SELECT * FROM teachers WHERE username = ?"
        cursor.execute(query, (name,))
        user_data = cursor.fetchone()

        if user_data is None or not check_password_hash(user_data['teacher_password'], password):
            flash('Foutieve gebruikersnaam/wachtwoord')
            return render_template('index.html')
        else:
            is_admin = user_data['is_admin']
            session['role'] = is_admin
            session['teacher_id'] = user_data['teacher_id']
            session['display_name'] = user_data['display_name']
            return redirect(url_for('notes.notes_overview', is_admin=is_admin))

    return render_template('index.html')

@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("U bent succesvol uitgelogd")
    return redirect(url_for("auth.index"))

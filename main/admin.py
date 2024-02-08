from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from database_functions import (get_teachers_from_db, insert_user_into_database, delete_user_from_database,
                                get_pw_username_is_admin_from_teachers)
from werkzeug.security import generate_password_hash

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.before_request
def before_admin_request():
    if 'teacher_id' in session:
        teacher_id = session['teacher_id']
        is_admin = get_pw_username_is_admin_from_teachers(teacher_id)
        if is_admin:
            return
    flash('U bent niet bevoegd deze pagina te bekijken')
    return redirect(url_for('notes.notes_overview'))


@admin_blueprint.route('/adminpage')
def admin_page():
    teachers = get_teachers_from_db()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(teachers) + per_page - 1) // per_page
    items_on_page = teachers[start:end]

    return render_template('admin.html', teachers=teachers, items_on_page=items_on_page,
                               total_pages=total_pages, page=page)


@admin_blueprint.route('/create-account', methods=['POST', 'GET'])
def create_teacher():
    return render_template('create-account.html')


@admin_blueprint.route("/insert-account", methods=['POST', 'GET'])
def insert_account():
    name_error = False
    username_error = False
    password_error = False
    if request.method == 'POST':
        name = request.form.get('name-teacher')
        username = request.form.get('username-teacher')
        password = request.form.get('password-teacher')
        hashed_password = generate_password_hash(password)
        admin_switch_value = request.form.get('admin-teacher', 'off')
        if admin_switch_value == 'on':
            admin = 1
        else:
            admin = 0
        if len(name) < 3:
            name_error = True
        if len(username) < 3:
            username_error = True
        if len(password) < 3:
            password_error = True

        if not name_error and not username_error and not password_error:
            msg = insert_user_into_database(name=name, username=username, password=hashed_password, admin=admin)
            return render_template('result-account.html', msg=msg)

    return render_template('create-account.html', name_error=name_error, username_error=username_error,
                           password_error=password_error)


@admin_blueprint.route("/delete-user/<teacher_id>", methods=['POST', 'GET'])
def delete_user(teacher_id):
    msg = delete_user_from_database(teacher_id)
    return render_template('result-account.html', msg=msg)

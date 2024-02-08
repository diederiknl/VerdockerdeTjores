from flask import Flask, request, redirect, session, url_for, flash
from auth import auth_blueprint
from notes import notes_blueprint
from admin import admin_blueprint

app = Flask(__name__)

app.secret_key = 'super secret key'
app.register_blueprint(auth_blueprint)
app.register_blueprint(notes_blueprint)
app.register_blueprint(admin_blueprint)


@app.before_request
def before_request():
    excluded_endpoints = ['auth.index', 'static']
    if request.endpoint in excluded_endpoints or 'teacher_id' in session:
        return
    flash('u moet ingelogd zijn om deze pagina te kunnen bekijken')
    return redirect(url_for('auth.index'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

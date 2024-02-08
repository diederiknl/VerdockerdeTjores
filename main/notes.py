from flask import Blueprint, render_template, request, session
from database_functions import *
from generate_question import generate_question

notes_blueprint = Blueprint('notes', __name__)

notes_data = {

    1: {'title': 'Note 1', 'content': 'This is the content of Note 1'},
    2: {'title': 'Note 2', 'content': 'This is the content of Note 2'},
}

@notes_blueprint.route('/notes-overview', methods=['POST', 'GET'])
def notes_overview():

    teacher_id = session.get('teacher_id')

    is_admin = request.args.get('is_admin', False)

    public_switch_filter = request.form.get('publicSwitchFilter', 'off')
    if public_switch_filter == 'on':
        notes_public = get_all_notes_from_database_where_not_public(teacher_id)
    else:
        notes_public = get_all_notes_from_database(teacher_id)

    teacher_switch_filter = request.form.get('teacherSwitchFilter', 'off')
    if teacher_switch_filter == 'on':
        notes_teacher = get_all_notes_from_database_every_teacher()
    else:
        notes_teacher = get_all_notes_from_database(teacher_id)

    notes = notes_public if public_switch_filter == 'on' else notes_teacher

    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(notes) + per_page - 1) // per_page
    items_on_page = notes[start:end]

    #Kijken voor ajax verzoek
    if 'X-Requested-With' in request.headers and request.headers['X-Requested-With'] == 'XMLHttpRequest':
        return render_template('notes-overview-ajax.html', notes=notes, items_on_page=items_on_page, total_pages=total_pages,
                               page=page, is_admin=is_admin, teacher_id=teacher_id)
    else:
        return render_template('notes-overview.html', notes=notes, items_on_page=items_on_page, total_pages=total_pages,
                               page=page, is_admin=is_admin, teacher_id=teacher_id)
    
@notes_blueprint.route('/create-note', methods=['POST', 'GET'])
def create_note():
    categories = get_all_categories_from_database()

    for category in range(0, len(categories)):
        if category == (len(categories) -1):
            checked_category = categories[len(categories)-1][0]
            categories.pop(category)

    return render_template('create-note.html', categories=categories, checked_category=checked_category)

@notes_blueprint.route("/insert", methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        connection = get_db()
        cursor = connection.cursor()
        title = request.form.get('note-title')
        source = request.form.get('note-source')
        public_switch_value = request.form.get('publicSwitch', 'off')
        if public_switch_value == 'on':
            public = 1
        else:
            public = 0
        question_switch_value = request.form.get('questionSwitch', 'off')
        if question_switch_value == 'on':
            question = 1
        else:
            question = 0
        teacher = session.get('teacher_id')
        note = request.form['note-text']
        category_id = None
        if request.form.get('categorySwitch') == 'on':
            new_category_name = request.form.get('note-category-text')
            if new_category_name:
                cursor.execute("INSERT INTO categories (omschrijving) VALUES (?)", (new_category_name,))
                connection.commit()
                category_id = get_category_id_from_database_by_name(new_category_name)
        else:
            category_name = request.form.get('note-category')
            if category_name:
                category_id = get_category_id_from_database_by_name(category_name)

        if category_id is None:
            msg = "Er is geen categorie toegevoegd of geselecteerd."
        else:
            msg = insert_note_into_database(title, source, public, teacher, note, category_id)

        return render_template('result.html', title=title, source=source, public=public,
                               teacher=teacher, note=note, category_id=category_id, msg=msg)

@notes_blueprint.route("/edit-note/<note_id>", methods=['POST', 'GET'])
def edit_note(note_id):
    notes = get_note_from_database_by_id(note_id)
    questions = get_question_from_database(notes[0]['note_id'])
    categories = get_all_categories_from_database()
    note_category = get_category_name_from_database_by_id(notes[0]['category_id'])
    public_access = get_public_access_from_database(notes[0]['note_id'])
    for category in categories:
        if category[0] == note_category:
            categories.remove(category)
        return render_template('edit-note.html', notes=notes, categories=categories, note_category=note_category, note_id=note_id, questions=questions, public_access=public_access)

@notes_blueprint.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        title = request.form.get('note-title')
        source = request.form.get('note-source')
        public_switch_value = request.form.get('publicSwitch', 'off')
        if public_switch_value == 'on':
            public = 1
        else:
            public = 0
        teacher = session.get('teacher_id')
        note = request.form['note-text']
        note_id = request.form.get('note_id')

        generate_question(note, note_id, request.form)

        if request.form.get('categorySwitch') == 'on':
            new_category_name = request.form.get('note-category-text')
            if new_category_name:
                category_id = add_category_to_database(new_category_name)
        else:
            category_name = request.form.get('note-category')
            if category_name:
                category_id = get_category_id_from_database_by_name(category_name)

        if category_id is None:
            msg = (f"Er is geen categorie toegevoegd of geselecteerd. "
                   f"categorySwitch: {request.form.get('categorySwitch')}, "
                   f"note-category: {request.form.get('note-category')}")
        else:
            msg = edit_note_in_database(title, source, public, teacher, note, note_id, category_id)

        return edit_note(note_id)

@notes_blueprint.route("/question_delete/<question_id><note_id>", methods=['POST', 'GET'])
def question_delete(question_id,note_id):
    delete_question_from_database_id(question_id)
    return edit_note(note_id)

@notes_blueprint.route("/question_edit/<question_id><note_id>", methods=['POST', 'GET'])
def question_edit(question_id,note_id):
    update_question_in_database(request.form.get(str(question_id)), question_id)
    return edit_note(note_id)

@notes_blueprint.route("/delete/<note_id>", methods=['POST'])
def delete(note_id):
    msg = delete_note_from_database(note_id)
    return render_template('result.html', msg=msg)


@notes_blueprint.route('/view-note/<note_id>', methods=['GET'])
def view_note(note_id):
    note_data = get_note_from_database_by_id(note_id)

    note = note_data[0] if note_data else {
        'title': None,
        'note_source': None,
        'is_public': None,
        'teacher_id': None,
        'category_id': None,
        'note': None
    }

    teacher_data = get_display_name_from_database(note['teacher_id'])
    category_data = get_category_name_from_database_by_id(note['category_id'])
    questions = get_question_from_database(note_data[0]['note_id'])

    return render_template('view-note.html', note=note, teacher_data=teacher_data, teacher=teacher_data,
                           category_data=category_data, note_id=note_id, questions=questions)
@notes_blueprint.route('/export-all-notes-csv')
def export_all_notes_csv():
    # zorgt ervoor dat het aanpast aan de searchbar
    search_criteria = request.args.get('search_criteria', '')

    filtered_notes = get_filtered_notes_from_database(search_criteria)

    if not filtered_notes:
        return render_template('error.html', message='Notes not found'), 404

    # maakt CSV data voor de specefieke note
    csv_data = "Title,Source,Teacher,Category,Note\n"
    for note in filtered_notes:
        csv_data += f'"{note["title"]}","{note["note_source"]}",{note["teacher_id"]},{note["category_id"]},"{note["note"]}"\n'

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=filtered_notes_export.csv'

    return response

@notes_blueprint.route('/export_note_csv/<int:note_id>', methods=['GET'])
def export_note_csv(note_id):
    note_data = get_note_from_database_by_id(note_id)

    # Als de note niet gevonden is
    if not note_data:
        return render_template('note-not-found.html')

    # Use the first element of the list
    note = note_data[0]

    # maakt CSV data voor de specefieke note
    csv_data = f"Title,Source,Teacher,Category,Note\n" \
               f'"{note["title"]}","{note["note_source"]}",{note["teacher_id"]},{note["category_id"]},"{note["note"]}"'

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=note_{note_id}_export.csv'

    return response

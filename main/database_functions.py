from flask import g
from flask import make_response
from io import StringIO
from flask import current_app
import sqlite3
import os
import csv

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'databases', 'testgpt.db')



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
        db.row_factory = sqlite3.Row
    return db


def get_all_categories_from_database():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT omschrijving FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    return categories


def get_display_name_from_database(teacher_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT display_name FROM teachers WHERE teacher_id=?", (teacher_id,))
    result = cursor.fetchone()
    cursor.close()

    display_name = result['display_name']
    return display_name

def get_category_id_from_database_by_name(category_name):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT category_id FROM categories WHERE omschrijving = ?", (category_name,))
    result = cursor.fetchone()
    cursor.close()
    category_id = result[0] if result else None
    cursor.close()
    return category_id

def get_public_access_from_database(note_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT is_public FROM notes WHERE note_id=?", (note_id,))
    result = cursor.fetchone()
    cursor.close()
    public_access = result['is_public']
    return public_access


def get_category_name_from_database_by_id(category_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT omschrijving FROM categories WHERE category_id = ?", (category_id,))
    result = cursor.fetchone()
    cursor.close()
    category = result[0] if result else None
    return category


def add_category_to_database(new_category_name):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categories (omschrijving) VALUES (?)", (new_category_name,))
    connection.commit()
    cursor.close()
    category_id = get_category_id_from_database_by_name(new_category_name)
    return category_id


def get_note_from_database_by_id(note_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT note_id, teacher_id, title, note_source, is_public, category_id, note FROM notes WHERE note_id=?",
        (note_id,))
    notes = cursor.fetchall()
    cursor.close()
    return notes

def get_filtered_notes_from_database(search_criteria):
    connection = get_db()
    cursor = connection.cursor()

    # Modify your database query to include search criteria
    query = "SELECT * FROM notes WHERE title LIKE ? OR note_source LIKE ? OR note LIKE ?"
    cursor.execute(query, ('%' + search_criteria + '%', '%' + search_criteria + '%', '%' + search_criteria + '%'))

    filtered_notes = cursor.fetchall()
    cursor.close()

    return filtered_notes

def get_all_notes_from_database(teacher_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT n.note_id, n.title, n.note_source, n.note, t.display_name, c.omschrijving, n.date_created, n.note_id, n.is_public FROM notes n JOIN teachers t ON n.teacher_id = t.teacher_id JOIN categories c ON n.category_id = c.category_id WHERE t.teacher_id=?', (teacher_id,))
    notes = cursor.fetchall()
    cursor.close()
    return notes

def get_all_notes_from_database_every_teacher():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT n.note_id, n.title, n.note_source, n.note, t.display_name, c.omschrijving, n.date_created, n.note_id, n.is_public FROM notes n JOIN teachers t ON n.teacher_id = t.teacher_id JOIN categories c ON n.category_id = c.category_id')
    notes = cursor.fetchall()
    cursor.close()
    return notes

def get_all_notes_from_database_where_not_public(teacher_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute('SELECT n.note_id, n.title, n.note_source, n.note, t.display_name, c.omschrijving, n.date_created, n.note_id, n.is_public FROM notes n JOIN teachers t ON n.teacher_id = t.teacher_id JOIN categories c ON n.category_id = c.category_id WHERE t.teacher_id=? AND n.is_public = 0', (teacher_id,))
    notes = cursor.fetchall()
    cursor.close()
    return notes


def delete_note_from_database(note_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes WHERE note_id = ?",
                       (note_id,))
        connection.commit()
        msg = "Notitie succesvol verwijderd uit de database"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the DELETE: {e}"
    finally:
        if connection:
            cursor.close()
            return msg


def edit_note_in_database(title, source, public, teacher, note, note_id, category_id,):
    connection = get_db()
    msg = ""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, note_source = ?, is_public = ?, teacher_id = ?, category_id = ?, note = ? WHERE note_id = ?",
            (title, source, public, teacher, category_id, note, note_id,))
        connection.commit()
        msg = "Notitie succesvol bijgewerkt in de database"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the EDIT: {e}"
    finally:
        if connection:
            cursor.close()
            return msg


def insert_note_into_database(title, source, public, teacher, note, category_id):
    connection = get_db()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO notes (title, note_source, is_public, teacher_id, category_id, note) VALUES (?, ?, ?, ?, ?, ?)",
                (title, source, public, teacher, category_id, note)
            )
        msg = "De notitie is succesvol opgeslagen"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = "Er is een fout opgetreden bij het opslaan van de notitie."
    finally:
        if connection:
            cursor.close()
            return msg

def get_pw_username_is_admin_from_teachers(teacher_id):
        connection = get_db()
        cursor = connection.cursor()
        query = "SELECT is_admin FROM teachers WHERE teacher_id = ?"
        cursor.execute(query, (teacher_id,))
        user_data = cursor.fetchone()
        if user_data and user_data[0] == 1:
            return True
        else:
            return False


def insert_question_into_database(question, note_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO questions (note_id, exam_question) VALUES (?,?)",
            (note_id, question))
        connection.commit()
        msg = "De notitie is succesvol opgeslagen"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        if connection:
            cursor.close()
            return msg

def get_question_from_database(note_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        query = "SELECT exam_question, questions_id FROM questions JOIN notes USING(note_id) WHERE note_id = ?"
        cursor.execute(query,(note_id,))
        question = cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        if connection:
            cursor.close()
        return question

def delete_question_from_database_id(question_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM questions WHERE questions_id = ?",
            (question_id,))
        connection.commit()
        msg = "De vraag is succesvol verwijderd"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the DELETE: {e}"
    finally:
        if connection:
            cursor.close()
            return msg

def update_question_in_database(question, question_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE questions SET exam_question = ? WHERE questions_id = ?",
            (question, question_id,))
        connection.commit()
        msg = "De vraag is succesvol geupdate"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the UPDATE: {e}"
    finally:
        if connection:
            cursor.close()
            return msg

def get_teachers_from_db():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    cursor.close()
    return teachers

def insert_user_into_database(name, username, password, admin):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO teachers (display_name, username, teacher_password, is_admin) VALUES (?,?,?,?)",
            (name, username, password, admin))
        connection.commit()
        msg = "De Gebruiker is succesvol opgeslagen"
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        msg = f"Error in the INSERT: {e}"
    finally:
        if connection:
            connection.close()
        return msg

def delete_user_from_database(teacher_id):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM teachers WHERE teacher_id = ?''', (teacher_id,))
        connection.commit()
        msg = "Record successfully deleted from the database"
    except Exception as e:
        msg = f"An error occurred: {str(e)}"
        connection.rollback()
    finally:
        if connection:
            connection.close()
        return msg
notes_database = [
    {'note_id': 1, 'title': 'Note 1', 'note_source': 'example.com', 'category_id': 1, 'teacher_id': 1, 'is_public': True, 'note_data': 'Content of Note 1'},
    {'note_id': 2, 'title': 'Note 2', 'note_source': 'example.com', 'category_id': 2, 'teacher_id': 2, 'is_public': False, 'note_data': 'Content of Note 2'},
    ]

def get_note_by_id(note_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes WHERE note_id=?", (note_id,))
    note_data = cursor.fetchone()
    cursor.close()
    return note_data

def export_note_csv(note_id):
    note = get_note_by_id(note_id)

    if note:
        
        #Chatgpt
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)

         # tot hier

        csv_writer.writerow(['note_id', 'title', 'note_source', 'category_id', 'teacher_id', 'is_public', 'note_data'])

        csv_writer.writerow([note['note_id'], note['title'], note['note_source'], note['category_id'],
                             note['teacher_id'], note['is_public'], note['note_data']])
       

        csv_string = csv_data.getvalue()

        csv_data.close()

        response = make_response(csv_string)

        response.headers["Content-Disposition"] = f"attachment; filename=note_{note_id}.csv"
        response.headers["Content-type"] = "text/csv"

        return response
    else:
        return "Note not found", 404

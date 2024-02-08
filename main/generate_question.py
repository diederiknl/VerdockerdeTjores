from database_functions import insert_question_into_database
from lib.testgpt.testgpt import TestGPT
# from apikey import api_key


def generate_question(note, note_id, form):
    test_gpt = TestGPT(api_key)

    if form.get('questionSwitch') == 'on':
        try:
            question = test_gpt._generate_question(note, 'open_question')
            insert_question_into_database(note_id=note_id, question=question)
        except Exception as e:
            print(e)

    elif form.get('MPquestionSwitch') == 'on':
        try:
            question = test_gpt._generate_question(note, 'multiple_choice_question')
            insert_question_into_database(note_id=note_id, question=question)
        except Exception as e:
            print(e)

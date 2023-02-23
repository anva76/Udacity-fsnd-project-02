import json
import uuid
import unittest
from models import db
from unittest import TestCase, mock
from app import app, ITEMS_PER_PAGE
from werkzeug.exceptions import InternalServerError

app.config.from_object('config.UnittestConfig')

db.app = app
db.init_app(app)

with app.app_context():
    db.create_all()


# 'Server error' side effect for unittest.mock
def abort_500_side_effect():
    abort(500)


class TestTrivia(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_categories(self):
        response = self.app.get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        response = self.app.get('/questions', query_string={'page': 1})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), ITEMS_PER_PAGE)

    def test_get_questions_by_category(self):
        response = self.app.get('/categories/1/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_add_new_question(self):
        test_question = 'test -' + uuid.uuid4().hex
        response = self.app.post('/questions',
                                 json={
                                   'question': test_question,
                                   'answer': 'test',
                                   'difficulty': 1,
                                   'category': 1,
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_question_search(self):
        # search for the previously added test question
        response = self.app.post('/questions',
                                 json={
                                   'search_term': 'test',
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) > 0)

    def test_delete_question(self):
        # add a new test question to be deleted
        test_question = 'test -' + uuid.uuid4().hex
        response = self.app.post('/questions',
                                 json={
                                  'question': test_question,
                                  'answer': 'test',
                                  'difficulty': 1,
                                  'category': 1,
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        question_id = data['question_id']

        # delete test question
        response = self.app.delete(f'/questions/{question_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_new_category(self):
        test_category = 'test -' + uuid.uuid4().hex[:8]
        response = self.app.post('/categories', json={
                                  'category': test_category
                                })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_category(self):
        # Add a new test category to be deleted
        test_category = 'test -' + uuid.uuid4().hex[:8]
        response = self.app.post('/categories',
                                 json={
                                   'category': test_category
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        category_id = data['category_id']

        # delete test category
        response = self.app.delete(f'/categories/{category_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_quizz_question(self):
        prev_questions = [16, 18]
        response = self.app.post('/quizzes',
                                 json={
                                  'quiz_category': {'id': 2, 'type': 'Art'},
                                  'previous_questions': prev_questions
                                  }
                                 )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotIn(data['question']['id'], prev_questions)

    def test_get_quizz_question_no_category(self):
        prev_questions = [16, 18, 4, 5, 9]
        response = self.app.post('/quizzes',
                                 json={
                                   'quiz_category': {'id': 0, 'type': ''},
                                   'previous_questions': prev_questions,
                                   }
                                 )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotIn(data['question']['id'], prev_questions)

    # Failure tests
    # -----------------------------------------------------------------
    @mock.patch('app.Category')
    def test_get_categories_fail(self, mock_model):
        # Mocking an internal server error
        mock_model.query.all.side_effect = InternalServerError('Mock error')

        response = self.app.get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    @mock.patch('app.Question')
    def test_get_questions_fail(self, mock_model):
        # Mocking an internal server error
        mock_model.query.order_by.return_value.all.side_effect =\
                   InternalServerError('Mock error')

        response = self.app.get('/questions', query_string={'page': 1})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category_fail(self):
        # category_id is out of range
        response = self.app.get('/categories/1000/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    @mock.patch('app.db.session')
    def test_add_new_question_fail(self, mock_session):
        # Mocking an internal server error
        mock_session.commit.side_effect = InternalServerError('Mock error')

        response = self.app.post('/questions',
                                 json={
                                   'question': 'test',
                                   'answer': 'test',
                                   'difficulty': 1,
                                   'category': 1,
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    @mock.patch('app.Question')
    def test_question_search_fail(self, mock_model):
        # Mocking an internal server error
        mock_model.query.filter.side_effect = InternalServerError('Mock error')

        response = self.app.post('/questions',
                                 json={
                                   'search_term': 'test',
                                 })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_delete_question_fail(self):
        # question id out of range
        response = self.app.delete('/questions/1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    @mock.patch('app.Question')
    def test_get_quiz_question_fail_500(self, mock_model):
        # Mocking an internal server error
        mock_model.query.filter.side_effect = InternalServerError('Mock error')

        response = self.app.post('/quizzes',
                                 json={
                                  'quiz_category': {'id': 2, 'type': 'Art'},
                                  'previous_questions': [16, 18]
                                  }
                                 )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_get_quiz_question_fail_400(self):
        # Invalid previous questions
        response = self.app.post('/quizzes',
                                 json={
                                  'quiz_category': {'id': 2, 'type': 'Art'},
                                  'previous_questions': [16, 1000]
                                  }
                                 )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

        # Invalid category
        response = self.app.post('/quizzes',
                                 json={
                                  'quiz_category': {'id': 100, 'type': 'Art'},
                                  'previous_questions': [16, 18]
                                  }
                                 )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()

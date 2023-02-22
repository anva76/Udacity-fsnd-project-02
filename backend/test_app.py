import unittest
import json
import uuid
from app import app, ITEMS_PER_PAGE
from models import db

TEST_DATABASE_URI = 'postgresql://dbuser:123@192.168.1.5:5432/trivia_test'

# connect SQLAlchemy to the test database URI
app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)

with app.app_context():
    db.create_all()


class TestTrivia(unittest.TestCase):

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
        response = self.app.post(
                                    '/questions',
                                    json={
                                        'question': test_question,
                                        'answer': 'test',
                                        'difficulty': 1,
                                        'category': 1,
                                    }
                                )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_question_search(self):
        # search for the previously added test question
        response = self.app.post(
                                    '/questions',
                                    json={
                                        'search_term': 'test',
                                    }
                                )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) > 0)

    def test_delete_question(self):
        # add a new test question to be deleted
        test_question = 'test -' + uuid.uuid4().hex
        response = self.app.post(
                                    '/questions',
                                    json={
                                        'question': test_question,
                                        'answer': 'test',
                                        'difficulty': 1,
                                        'category': 1,
                                    }
                                )
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
                            }
                        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_category(self):
        # Add a new test category to be deleted
        test_category = 'test -' + uuid.uuid4().hex[:8]
        response = self.app.post('/categories', json={
                                'category': test_category
                            }
                        )
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
        response = self.app.post(
                                    '/quizzes',
                                    json={
                                        'quiz_category': {
                                                'id': 2,
                                                'type': 'Art'
                                              },
                                        'previous_questions': prev_questions,
                                    }
                                )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotIn(data['question']['id'], prev_questions)

    def test_get_quizz_question_no_category(self):
        prev_questions = [16, 18, 4, 5, 9]
        response = self.app.post(
                                    '/quizzes',
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


if __name__ == "__main__":
    unittest.main()

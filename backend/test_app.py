import unittest
import json
from app import app, ITEMS_PER_PAGE

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
        response = self.app.get('/questions', query_string={'page':1})
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
        response = self.app.post('/questions', 
                                    json={
                                        'question':'test', 'answer':'test',
                                        'difficulty':1, 'category': 1,
                                    }
                                )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data['success'], True)

    def test_question_search(self):
        # search for the previously added test question
        response = self.app.post('/questions', json={
                                        'search_term':'test', 
                                    }
                                )       

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) > 0)        

    def test_delete_question(self):
        # add a new test question to be deleted
        response = self.app.post('/questions', json={
                                        'question':'test', 'answer':'test',
                                        'difficulty':1, 'category': 1,
                                    }
                                )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.question_id = data['question_id']

        # delete test question
        response = self.app.delete(f'/questions/{self.question_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data['success'], True)

    def test_get_quizz_question(self):
        prev_questions = [16,18]
        response = self.app.post('/quizzes', json={
                                        'quiz_category': {'id':2, 'type':'Art'},
                                        'previous_questions': prev_questions,
                                    }
                                )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotIn(data['question']['id'], prev_questions)

    def test_get_quizz_question_no_category(self):
        prev_questions = [16,18,4,5,9]
        response = self.app.post('/quizzes', json={
                                        'quiz_category': {'id':0,'type':"all"},
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

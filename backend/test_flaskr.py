import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_book = {
            'question': 'What is the airspeed velocity...',
            'answer':'blah', 
            'category':'1', 
            'difficulty': 3,
            }
        self.search_with_results = {
            'searchTerm': 'Tim',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
   
    def test_get_paginated_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
    
    def test_404_sent_requestion_beyond_valid_page(self):
        res = self.client().get('/api/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error_code'], 404)

    def test_get_categories_200(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])

# TODO: Figure out how to mimic nothing in the db. Maybe run this after clearing the db?
    # def test_get_categores_404(self):
    #     res = self.client().get('/api/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code,404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    #     self.assertEqual(data['error_code'], 404)

#   TEST: When you submit a question on the "Add" tab, 
#   the form will clear and the question will appear at the end of the last page
#   of the questions list in the "List" tab.  
    def test_delete_question(self):
        res = self.client().delete('/api/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['question']))
        self.assertEqual(question, None)

    def test_delete_question_out_of_scope(self):
        # Should return 422
        res = self.client().delete('/api/questions/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(data['error_code'], 422)


    def test_create_question_success(self):
        
        res = self.client().post('/api/questions', json=self.new_book)
       
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_info'])
        self.assertTrue(data['total_questions'])



    def test_get_question_search_with_results(self):
        res = self.client().post('/api/questions/search', json=self.search_with_results)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       # self.assertTrue(data['total_books'])
        #self.assertEqual(len(data['books']), 4)
        #curl localhost:3000/api/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "tim"}'
    def test_get_question_search_without_results(self):
        res = self.client().post('/api/questions/search', json={'searchTerm': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    def test_get_category_questions_success(self):
        res = self.client().post('/api/categories/1/questions', json={'id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], 1)
        

  #  def test_get_category_questions_out_of_scope(self):





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  curr_questions = questions[start:end]
  return curr_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/') 
  def hello():
    return jsonify({'message': 'Hello there. You can find api documentation at: https://github.com/SethW89/udacity_trivia_api'})
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def get_categories():
    selection = Category.query.order_by(Category.id).all()
    categories = {category.id : category.type for category in selection}

    if categories == []:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': categories,
      'total_categories': len(Category.query.all())
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions')
  def get_questions():

    selection = Question.query.order_by(Question.id).all()
    curr_questions = paginate_questions(request, selection)
    selection = Category.query.order_by(Category.id).all()
    categories = {category.id : category.type for category in selection}
    #print(categories)
    if curr_questions == []:
      abort(404)
      
    return jsonify({
      'success': True,
      'questions': curr_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories,
      'current_category': None,
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    selection = Question.query.get(question_id)
    #print(selection)
    if selection is None:
      abort(404)
    try:
      selection = Question.query.get(question_id)
      question = selection.format()
      selection.delete()
      
      return jsonify({
        'success': True,
        'deleted': question_id,
        'question': question,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    if (question == '') or (answer == '') or (category == '') or (difficulty == ''):
        abort(400)

    try:
      item = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      item.insert()

      return jsonify({
        'success': True,
        'created': item.id,
        'question_info': item.format(),
        'total_questions': len(Question.query.all())
      })
    except:
      abort(500)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only questions that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def search_questions():
    #print('search_questions()')
    body = request.get_json()
    search = body.get('searchTerm', None)
    #print(body.get('searchTerm', None)
    if search:
      selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
      selected_questions = paginate_questions(request, selection)
      #print(len(selection.all()))

      return jsonify({
        'success': True,
        'questions': selected_questions,
        'total_questions': len(selection.all()),
        'current_category': None,
      })
    else:
      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
    if len(selection) == 0:
      abort(404)
    curr_questions = paginate_questions(request, selection)
 
    return jsonify({
      'success': True,
      'questions': curr_questions,
      'total_questions': len(selection),
      'current_category': category_id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def start_quiz():
    try:
      body = request.get_json()
      previous_questions = body['previous_questions']
      quiz_category = body['quiz_category']
      quiz_category_id = int(quiz_category['id'])
      if quiz_category_id > 6:
        abort(400)
      if quiz_category_id != 0:
        quiz_questions = Question.query.filter_by(
          category=quiz_category_id
          ).filter(
          Question.id.notin_(previous_questions)
          ).all()
      else:
        quiz_questions = Question.query.all()
      # Check if we are out of questions.
      if len(previous_questions) == len(quiz_questions):
        return jsonify({
          'success': True,
          'question': None
        })
      # FORMAT and send out the next question.
      question = random.choice(quiz_questions).format()
      # print({
      #   'success': True,
      #   'question': question,
      #   'previous_questions': previous_questions,
      # })
      return jsonify({
        'success': True,
        'question': question,
        'previous_questions': previous_questions,
      })

    except:
      abort(400)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
        'success': False,
        'error_code': 400,
        'message': 'bad request'
      }), 400
      
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error_code': 404,
        'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error_code': 405,
        'message': 'method not allowed'
      }), 405
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error_code': 422,
        'message': 'unprocessable'
      }), 422
  
  return app

    
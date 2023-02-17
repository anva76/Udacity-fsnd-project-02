from flask import Flask, jsonify, request, abort
from models import db, Category, Question
from flask_cors import CORS
import random
#from flask_migrate import Migrate

ITEMS_PER_PAGE = 10

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
#migrate = Migrate(app, db)
#CORS(app)
CORS(app, resources={r'/api/*' : {'origins': '*'}})

# Error response with a specific message and code
def error_response(message, code):
	return jsonify({
		'success': False,
		'error': code,
		'message': message
	}),code

# Paginator
# ---------------------------------------------------------------
def paginator(request, selection):
	page = request.args.get('page', 1, int)
	start = (page - 1) * ITEMS_PER_PAGE
	end = start + ITEMS_PER_PAGE
	
	if start > len(selection) - 1:
		return None
	else:
		rows = [i.format() for i in selection]
		return rows[start:end]

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

# List all categories
# ---------------------------------------------------------------------
#@cross_origin
@app.route('/categories', methods=['GET'])
def get_categories():
	categories = Category.query.all()

	data = {
		'success': True,
		'categories': {	c.id: c.type for c in categories }
	}
	
	return jsonify(data)

# List questions by category
# ---------------------------------------------------------------------
@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
	category = Category.query.get_or_404(category_id)
	questions = Question.query.filter(Question.category == category.id).all()

	data = {
		'success': True,
		'questions': [q.format() for q in questions],
		'total_questions': len(questions),
		'current_category': category.type
	}

	return jsonify(data)

# List questions by page
# ---------------------------------------------------------------------
@app.route('/questions', methods=['GET'])
def get_questions_paginated():
	questions = Question.query.all()
	questions_by_page = paginator(request, questions)

	if questions_by_page is None:
		abort(404)

	categories = Category.query.all()

	data = {
		'success': True,
		'questions': questions_by_page,
		'total_questions': len(questions),
		'categories': {	c.id: c.type for c in categories },
		'current_category': '',
	}

	return jsonify(data)

# Delete a specific question
# ---------------------------------------------------------------------
@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
	error = False
	question = Question.query.get_or_404(question_id)
	
	try:
		question.delete()
	except:
		error = True
		db.session.rollback()
		print(sys.exc_info())	
	finally:
		db.session.close()
		
	if error:
		return error_response(f'Server error. Question id:{question.id} could not be deleted.', 500) 
	else:
		return jsonify ({
			'success': True,
		})

# Validate question data from request body
# ---------------------------------------------------------------------
def validate_question_data(request):
	body = request.get_json()
	print(body)

	question = body.get('question', None)
	answer = body.get('answer', None)
	difficulty = body.get('difficulty', None)
	category = body.get('category', None)
	
	if not all([question, answer, difficulty, category]):
		return None
		
	# Assert integer values
	try:
		difficulty = int(difficulty)
		category = int(category)
	except ValueError:
		return None
		
	return {
		'question': question,
		'answer': answer,
		'difficulty': difficulty,
		'category': category
	}

# POST /questions endpoint
# ---------------------------------------------------------------------
@app.route('/questions', methods=['POST'])
def dispatch_post_questions():
	if 'search_term' in request.get_json():
		return search_questions(request)
	else:
		return add_question(request)

# Add a new question
# ---------------------------------------------------------------------
def add_question(request):
	error = False	
	question_data = validate_question_data(request)
	if question_data is None:
		abort(400)
		
	category = Category.query.filter(Category.id == question_data['category']).one_or_none()
	if category is None:
		return error_response('Category not found', 404)
		
	try:
		question = Question()
		question.populate_from_dict(question_data)
		question.insert()
	except:
		error = True
		db.session.rollback()
		print(sys.exc_info())	
	finally:
		db.session.close()	

	if error:
		return error_response(f'Server error. New question could not be created.', 500) 
	else:		
		return jsonify ({
			'succuess': True
		})

# Search questions
# ---------------------------------------------------------------------
def search_questions(request):
	search_term = request.get_json()['search_term']
	
	questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
	
	data = {
		'success': True,
		'questions': [q.format() for q in questions],
		'total_questions': len(questions),
		'current_category': ''
	}
	
	return jsonify(data)

# Get the next question
# ---------------------------------------------------------------------
@app.route('/quizzes', methods=['POST'])
def get_next_question():
	category_id = request.get_json()['quiz_category']['id']
	previous_questions = request.get_json()['previous_questions']
	print(category_id, previous_questions)
	
	category = Category.query.filter(Category.id == category_id).one_or_none()
	if category is None:
		return error_response('Category not found', 404)	
		
	all_question_ids = [
		q.id
		for q in Question.query.filter(Question.category == category_id).all()
	]
	print(all_question_ids)
		
	if not set(previous_questions).issubset(all_question_ids):
		return error_response('Invalid previous questions', 404)		
		
	next_question_pool = set(all_question_ids).difference(previous_questions)
	print(next_question_pool)

	if len(next_question_pool) != 0:
		question_id = random.choice(list(next_question_pool))
		question = (Question.query.filter(Question.id == question_id).one()).format()
	else:
		question = None
			
	return jsonify ({
		'success': True,
		'question': question,
	})

# Default error handlers
# ---------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
	return jsonify({
		'success': False,
		'error': 404,
		'message': 'Not found',
	}),404

@app.errorhandler(400)
def bad_request(error):
	return jsonify({
		'success': False,
		'error': 400,
		'message': 'Invalid request',
	}),400


# Default port:
if __name__ == '__main__':
    app.run()

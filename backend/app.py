from flask import Flask, jsonify, request, abort
from models import db, Category, Question, create_tables
from flask_cors import CORS
from sqlalchemy import func as fn
import random

ITEMS_PER_PAGE = 10

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS'
    )
    return response


# Error response with a specific message and code
def error_response(message, code):
    return jsonify({
        'success': False,
        'error': code,
        'message': message
    }), code


# Paginator
# ---------------------------------------------------------------
def paginator(request, selection):
    page = request.args.get('page', 1, int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    rows = [i.format() for i in selection]
    if start > len(selection) - 1:
        # return the first page if the page number is out of range
        return rows[0:ITEMS_PER_PAGE], 1
    else:
        return rows[start:end], page


# List all categories
# ---------------------------------------------------------------------
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    data = {
        'success': True,
        'categories': {c.id: c.type for c in categories}
    }
    return jsonify(data)


# List questions by category
# ---------------------------------------------------------------------
@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_by_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        abort(404)

    questions = Question.query.order_by(
                                    Question.id
                               ).filter(
                                    Question.category == category.id
                               ).all()

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
    questions = Question.query.order_by(Question.id).all()
    questions_by_page, actual_page = paginator(request, questions)

    categories = Category.query.all()

    data = {
        'success': True,
        'questions': questions_by_page,
        'total_questions': len(questions),
        'categories': {c.id: c.type for c in categories},
        'current_category': '',
        'actual_page': actual_page,
    }

    return jsonify(data)


# Delete a specific question
# ---------------------------------------------------------------------
@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    error = False
    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)

    try:
        question.delete()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        return error_response(
            f'Server error. Question id:{question.id} could not be deleted.',
            500
          )
    else:
        return jsonify({
            'success': True,
        })


# Validate question data from request body
# ---------------------------------------------------------------------
def validate_question_data(request):
    body = request.get_json()
    # print(body)
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

    category = Category.query.filter(
                    Category.id == question_data['category']
                ).one_or_none()

    if category is None:
        return error_response('Category not found', 404)

    try:
        question = Question()
        question.populate_from_dict(question_data)
        question.insert()
        question_id = question.id
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        return error_response(
                'Server error. New question could not be created.',
                500
              )
    else:
        return jsonify({
            'success': True,
            'question_id': question_id,
        })


# Search questions
# ---------------------------------------------------------------------
def search_questions(request):
    search_term = request.get_json()['search_term']

    questions = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')
                ).all()

    data = {
        'success': True,
        'questions': [q.format() for q in questions],
        'total_questions': len(questions),
        'current_category': ''
    }

    return jsonify(data)


# Add a new category
# ---------------------------------------------------------------------
@app.route('/categories', methods=['POST'])
def add_category():
    error = False
    category_type = request.get_json().get('category', None)
    if not category_type:
        abort(400)

    category = Category.query.filter(
                fn.lower(Category.type) == fn.lower(category_type)
            ).one_or_none()
    if category:
        return error_response(
                f"Category '{category_type}' already exists.",
                400
              )

    try:
        category = Category(category_type)
        category.insert()
        category_id = category.id
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        return error_response(
            'Server error. New category could not be created.',
            500
          )
    else:
        return jsonify({
            'success': True,
            'category_id': category_id,
        })


# Delete a specific category
# ---------------------------------------------------------------------
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    error = False
    category = db.session.get(Category, category_id)
    if category is None:
        abort(404)

    try:
        category.delete()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        return error_response(
            f"Server error. Category id'{category_id} could not be deleted.'",
            500
        )
    else:
        return jsonify({
            'success': True,
        })


# Validate quiz data
# ---------------------------------------------------------------------
def validate_quiz_data(request):
    data = request.get_json()
    # print(data)

    category = data.get('quiz_category', None)
    if category:
        category_id = category['id']
    else:
        category_id = None

    previous_questions = data.get('previous_questions', None)

    if previous_questions is None or category_id is None:
        return False, None, None

    # Assert integer values
    try:
        category_id = int(category_id)
        previous_questions_int = [int(q) for q in previous_questions]
    except ValueError:
        return False, None, None

    return True, category_id, previous_questions_int


# Get the next question
# ---------------------------------------------------------------------
@app.route('/quizzes', methods=['POST'])
def get_next_question():
    result, category_id, previous_questions = validate_quiz_data(request)
    if not result:
        abort(400)
    # print(category_id, previous_questions)

    if category_id == 0:
        all_question_ids = [
            q.id
            for q in Question.query.all()
        ]
    else:
        category = Category.query.filter(
                Category.id == category_id
             ).one_or_none()
        if category is None:
            return error_response('Category not found', 404)

        all_question_ids = [
            q.id
            for q in Question.query.filter(
                    Question.category == category_id
                 ).all()
        ]
    # print(all_question_ids)

    if not set(previous_questions).issubset(all_question_ids):
        return error_response('Invalid previous questions', 400)

    next_question_pool = set(all_question_ids).difference(previous_questions)
    # print(next_question_pool)

    if len(next_question_pool) != 0:
        question_id = random.choice(list(next_question_pool))
        question = Question.query.filter(Question.id == question_id).one()
    else:
        question = None

    return jsonify({
        'success': True,
        'question': question.format(),
    })


# Default error handlers
# ---------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found',
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Invalid request',
    }), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error',
    }), 500


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity',
    }), 422


if __name__ == '__main__':
    app.config.from_object('config')
    db.init_app(app)
    with app.app_context():
        create_tables()
    app.run()

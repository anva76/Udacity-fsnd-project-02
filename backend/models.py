#from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_tables():
    db.create_all()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, question=None, answer=None, category=None, difficulty=None):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        
    def populate_from_dict(self, data):
      for key, value in data.items():
        setattr(self, key, value)    	

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }





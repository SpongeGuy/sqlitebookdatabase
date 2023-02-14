from flask import Flask, request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

basedir = os.path.abspath(os.path.dirname(__file__))
path = basedir + '/tmp'
if not os.path.exists(basedir + '/tmp'):
	os.makedirs(path)

db = SQLAlchemy(app)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	author = db.Column(db.String(80), unique=True, nullable=False)
	publisher = db.Column(db.String(80), unique=True, nullable=False)

	def __repr__(self):
		return f"{self.name}\n{self.author}\n{self.publisher}"

def add_book(book):
	try:
		db.session.add(book)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return "Error: book already exists with that name"
	return "book added successfully"

with app.app_context():
	db.create_all()
	book = Book(name="harry potter", author="jk rowling", publisher="johnbook inc")
	#add_book(book)
	
	books = Book.query.all()
	print(books)



@app.route('/')
def index():
	return 'Hello!'

# http://urlhere.com/books
@app.route('/books')
def get_books():
	books = Book.query.all()
	output = []
	for book in books:
		book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}
		output.append(book_data)
	return {"books": output}

@app.route('/books/<id>')
def get_book(id):
	book = Book.query.get_or_404(id)
	return {"name": book.name, "author": book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
	book = Book(name=request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
	db.session.add(book)
	db.session.commit()
	return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
	book = Book.query.get(id)
	if book is None:
		return {"error": 404}
	db.session.delete(book)
	db.session.commit()
	return {"message": "ur done buddy"}

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
	book = Book.query.get(id)
	if book is None:
		return {"error": 404}
	new_book = Book(name=request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
	book.name = new_book.name
	book.author = new_book.author
	book.publisher = new_book.publisher
	db.session.commit()
	return {"message": "target assimilated"}
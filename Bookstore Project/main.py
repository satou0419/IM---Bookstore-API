from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Change this to your username:password@localhost:port/db name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Rdgg0419@localhost:3306/dbbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Define a route for the root URL
@app.route('/')
def index():
    return 'Welcome to the Bookstore API!'

# Define a route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Books.query.all()
    result = [{'Title': book.Title, 'Author': book.Author, 'Price': book.Price} for book in books]
    return jsonify(result)

# Define a route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('Title')
    author = data.get('Author')
    price = data.get('Price')

    new_book = Books(Title=title, Author=author, Price=price)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

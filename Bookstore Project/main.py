from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Rdgg0419@localhost:3306/dbbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('category.CategoryID'))
    Category = db.relationship('Category', back_populates='books')

class Category(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', back_populates='Category')

class AuditTrail(db.Model):
    __tablename__ = 'AuditTrail'  # Explicitly set the table name
    AuditID = db.Column(db.Integer, primary_key=True)
    Action = db.Column(db.String(255))
    ObjectType = db.Column(db.String(255))
    ObjectID = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())



# Create tables
with app.app_context():
    db.create_all()
    db.session.commit()

# Define a route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [{'Title': book.Title, 'Author': book.Author, 'Price': book.Price, 'Category': {'CategoryName': book.Category.CategoryName}} for book in books]
    return jsonify(result)

# Define a route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('Title')
    author = data.get('Author')
    price = data.get('Price')
    category_name = data.get('Category')

    # Check if the category exists, if not create a new one
    category = Category.query.filter_by(CategoryName=category_name).first()
    if not category:
        category = Category(CategoryName=category_name)
        db.session.add(category)
        db.session.commit()

    new_book = Book(Title=title, Author=author, Price=price, Category=category)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully!'})

# Define a route to update a book
@app.route('/books/<string:title>', methods=['PUT'])
def update_book(title):
    book = Book.query.filter_by(Title=title).first()
    if book:
        data = request.json
        book.Title = data.get('Title', book.Title)
        book.Author = data.get('Author', book.Author)
        book.Price = data.get('Price', book.Price)
        
        category_name = data.get('Category')
        # Check if the category exists, if not create a new one
        category = Category.query.filter_by(CategoryName=category_name).first()
        if not category:
            category = Category(CategoryName=category_name)
            db.session.add(category)
        
        book.Category = category
        
        db.session.commit()
        return jsonify({'message': 'Book updated successfully!'})
    else:
        return jsonify({'error': 'Book not found'}), 404

# Define a route to delete a book
@app.route('/books/<string:title>', methods=['DELETE'])
def delete_book(title):
    book = Book.query.filter_by(Title=title).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully!'})
    else:
        return jsonify({'error': 'Book not found'}), 404

# Define a route to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = [{'CategoryName': category.CategoryName} for category in categories]
    return jsonify(result)

# Define a route to add a new category
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    category_name = data.get('CategoryName')
    new_category = Category(CategoryName=category_name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully!'})

# Define a route to get the audit trail
@app.route('/audit-trail', methods=['GET'])
def get_audit_trail():
    audit_trail = AuditTrail.query.all()
    result = [{'AuditID': entry.AuditID, 'Action': entry.Action, 'ObjectType': entry.ObjectType, 'ObjectID': entry.ObjectID, 'Timestamp': entry.Timestamp} for entry in audit_trail]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
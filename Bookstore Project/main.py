# Import required libraries
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Add this line
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app)
# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40Rdgg0419@localhost:3306/dbbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('category.CategoryID'))
    Category = db.relationship('Category', back_populates='books')

# Define the Category model
class Category(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', back_populates='Category')

# Define the AuditTrail model
class AuditTrail(db.Model):
    __tablename__ = 'Audit'
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
    result = [{'BookID': book.BookID, 'Title': book.Title, 'Author': book.Author, 'Price': book.Price, 'Category': {'CategoryName': book.Category.CategoryName}} for book in books]
    return jsonify(result)

# Define a route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('Title')
    author = data.get('Author')
    price = data.get('Price')
    category_name = data.get('Category')

    # Call the stored procedure for adding a book
    db.session.execute(db.text(f"CALL AddBook('{title}', '{author}', {price}, '{category_name}')"))
    db.session.commit()

    return jsonify({'message': 'Book added successfully!'})

# Define a route to update a book using the stored procedure
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    title = data.get('Title')  # Add this line to get the new title
    author = data.get('Author')
    price = data.get('Price')
    category_name = data.get('Category')

    # Call the stored procedure using text
    db.session.execute(text(f"CALL UpdateBook({book_id}, '{title}', '{author}', {price}, '{category_name}')"))
    db.session.commit()

    return jsonify({'message': 'Book updated successfully!'})




# Modify the route to accept book_id as a path parameter
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Call the stored procedure for deleting a book using book_id
    db.session.execute(db.text(f"CALL DeleteBook({book_id})"))
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully!'})



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

    # Call the stored procedure for adding a category
    db.session.execute(db.text(f"CALL AddCategory('{category_name}')"))
    db.session.commit()

    return jsonify({'message': 'Category added successfully!'})

#ROUTE OF VIEWS

@app.route('/audit-trail-view', methods=['GET'])
def get_audit_trail_view():
    audit_trail_view = db.session.execute(text('SELECT * FROM vw_audit_trail')).fetchall()
    result = [{'AuditID': entry.AuditID, 'Message': entry.Message, 'ObjectType': entry.ObjectType, 'ObjectID': entry.ObjectID, 'Timestamp': entry.Timestamp} for entry in audit_trail_view]
    return jsonify(result)

# Define a route to get all books from the view
@app.route('/books-view', methods=['GET'])
def get_books_from_view():
    books = db.session.execute(text('SELECT * FROM vw_books')).fetchall()
    result = [
        {'BookID': book.BookID, 'Title': book.Title, 'Author': book.Author, 'Price': book.Price, 'Category': book.Category}
        for book in books
    ]
    return jsonify(result)


# Define a route to get category statistics
@app.route('/category-stats', methods=['GET'])
def get_category_stats():
    category_stats = db.session.execute(text('SELECT * FROM vw_category_stats')).fetchall()
    result = [{'CategoryName': entry.CategoryName, 'TotalBooks': entry.TotalBooks, 'CreationDate': entry.CreationDate} for entry in category_stats]
    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

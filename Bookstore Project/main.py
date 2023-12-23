# Import required libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import text


# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/dbbook'
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

    # Define the Audit model
class Audit(db.Model):
    AuditID = db.Column(db.Integer, primary_key=True)
    Action = db.Column(db.String(255))
    ObjectType = db.Column(db.String(255))
    ObjectID = db.Column(db.Integer)
    Timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


# Create tables
with app.app_context():
    db.create_all()
    db.session.commit()

# ... (Routes will be added here)


@app.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    audit_logs = db.session.execute(text('SELECT * FROM audit')).fetchall()
    result = [{'ID': entry.AuditID, 'Message': entry.Action, 'Object Type': entry.ObjectType, 'Object ID': entry.ObjectID, 'Date': entry.Timestamp} for entry in audit_logs]
    return jsonify(result)


# Define a route to get category statistics
@app.route('/category-stats', methods=['GET'])
def get_category_stats():
    category_stats = db.session.execute(text('SELECT * FROM vw_category_stats')).fetchall()
    result = [{'CategoryName': entry.CategoryName, 'TotalBooks': entry.TotalBooks, 'CreationDate': entry.CreationDate} for entry in category_stats]
    return jsonify(result)


    
    # Define a route to get a specific book by ID
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
    db.session.execute(db.text(f"CALL AddBookProcedure('{title}', '{author}', {price}, '{category_name}')"))
    db.session.commit()

    return jsonify({'message': 'Book added successfully!'})

# Define a route to update a book using the stored procedure
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    title = data.get('Title')
    author = data.get('Author')
    price = data.get('Price')
    category_name = data.get('Category')

    # Call the stored procedure using text
    db.session.execute(text(f"CALL UpdateBookProcedure({book_id}, '{title}', '{author}', {price}, '{category_name}')"))
    db.session.commit()

    return jsonify({'message': 'Book updated successfully!'})

# Define a route to delete a book by ID
# Define a route to delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        # Log the delete action in the Audit table
        db.session.execute(
            text(f"CALL DeleteBookProcedure({book_id})")
        )
        db.session.commit()
        
        return jsonify({'message': 'Book deleted successfully!'})
    else:
        return jsonify({'error': 'Book not found'}), 404
    

    # Define a route to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = [{'CategoryID': category.CategoryID, 'CategoryName': category.CategoryName} for category in categories]
    return jsonify(result)

# Define a route to add a new category
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    category_name = data.get('CategoryName')

    # Check if the category already exists
    existing_category = Category.query.filter_by(CategoryName=category_name).first()
    if existing_category:
        return jsonify({'error': 'Category already exists'}), 400

    # Create a new category
    new_category = Category(CategoryName=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Category added successfully!', 'CategoryID': new_category.CategoryID})

# Define a route to update a category
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    new_category_name = data.get('CategoryName')

    # Check if the category exists
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    # Update the category name
    category.CategoryName = new_category_name
    db.session.commit()

    return jsonify({'message': 'Category updated successfully!'})

# Define a route to delete a category
@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully!'})
    else:
        return jsonify({'error': 'Category not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, abort

# Initialize Flask application
app = Flask(__name__)

# Configuration
# Use environment variable for secret key in production, with a default for local development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'online-bookstore-secret-key-2026')
# SQLite database path (can be overridden in tests)
app.config['DATABASE'] = os.environ.get('DATABASE_PATH', os.path.join(app.root_path, 'database.db'))


def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Row factory is set to sqlite3.Row so columns can be accessed by name.
    """
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database schema and seeds initial sample books
    if the database is newly created or empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create books table if it does not already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Check if any books exist
    cursor.execute('SELECT COUNT(*) AS count FROM books')
    count = cursor.fetchone()['count']

    # Seed initial sample data if table is empty
    if count == 0:
        sample_books = [
            ('To Kill a Mockingbird', 'Harper Lee', 12.99, 15),
            ('1984', 'George Orwell', 10.50, 24),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 9.99, 8),
            ('Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', 34.50, 5),
            ('The Pragmatic Programmer', 'David Thomas & Andrew Hunt', 39.99, 3),
            ('Automate the Boring Stuff with Python', 'Al Sweigart', 25.00, 12),
            ('Computer Networking: A Top-Down Approach', 'James Kurose & Keith Ross', 49.99, 4)
        ]
        cursor.executemany('''
            INSERT INTO books (title, author, price, quantity)
            VALUES (?, ?, ?, ?)
        ''', sample_books)
        conn.commit()

    conn.close()


def validate_book_data(title, author, price_str, quantity_str):
    """
    Validates form data for adding or editing a book.
    Returns: (is_valid: bool, errors: list[str], cleaned_data: dict)
    """
    errors = []
    cleaned = {}

    # Validate Title
    if not title or not title.strip():
        errors.append("Book title is required.")
    elif len(title.strip()) > 200:
        errors.append("Book title must be less than 200 characters.")
    else:
        cleaned['title'] = title.strip()

    # Validate Author
    if not author or not author.strip():
        errors.append("Author name is required.")
    elif len(author.strip()) > 150:
        errors.append("Author name must be less than 150 characters.")
    else:
        cleaned['author'] = author.strip()

    # Validate Price
    if not price_str or not str(price_str).strip():
        errors.append("Price is required.")
    else:
        try:
            price = float(price_str)
            if price <= 0:
                errors.append("Price must be a positive number greater than 0.")
            elif price > 100000:
                errors.append("Price cannot exceed $100,000.00.")
            else:
                cleaned['price'] = round(price, 2)
        except (ValueError, TypeError):
            errors.append("Price must be a valid numeric value (e.g., 14.99).")

    # Validate Quantity
    if quantity_str is None or str(quantity_str).strip() == "":
        errors.append("Quantity is required.")
    else:
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                errors.append("Quantity cannot be negative.")
            elif quantity > 100000:
                errors.append("Quantity cannot exceed 100,000 units.")
            else:
                cleaned['quantity'] = quantity
        except (ValueError, TypeError):
            errors.append("Quantity must be a valid whole number (e.g., 10).")

    is_valid = len(errors) == 0
    return is_valid, errors, cleaned


# Ensure database is initialized at startup
init_db()


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.route('/')
def index():
    """
    Display all books in the inventory, along with summary statistics.
    Supports optional server-side search query string (?q=...).
    """
    search_query = request.args.get('q', '').strip()
    conn = get_db_connection()

    if search_query:
        query_param = f"%{search_query}%"
        books = conn.execute(
            '''SELECT * FROM books 
               WHERE title LIKE ? OR author LIKE ? 
               ORDER BY id DESC''',
            (query_param, query_param)
        ).fetchall()
    else:
        books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()

    # Compute inventory summary statistics
    all_books = conn.execute('SELECT price, quantity FROM books').fetchall()
    conn.close()

    total_titles = len(all_books)
    total_stock_units = sum(b['quantity'] for b in all_books)
    total_inventory_value = sum(b['price'] * b['quantity'] for b in all_books)
    low_stock_count = sum(1 for b in all_books if b['quantity'] < 5)

    stats = {
        'total_titles': total_titles,
        'total_stock_units': total_stock_units,
        'total_inventory_value': total_inventory_value,
        'low_stock_count': low_stock_count
    }

    return render_template('index.html', books=books, stats=stats, search_query=search_query)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    Add a new book to the inventory.
    GET: Render the addition form.
    POST: Validate inputs and insert into SQLite database.
    """
    if request.method == 'POST':
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')

        is_valid, errors, cleaned = validate_book_data(title, author, price, quantity)

        if not is_valid:
            for error in errors:
                flash(error, 'danger')
            # Retain user inputs so they don't have to retype everything
            return render_template('add_book.html', form_data=request.form), 400

        try:
            conn = get_db_connection()
            conn.execute(
                '''INSERT INTO books (title, author, price, quantity)
                   VALUES (?, ?, ?, ?)''',
                (cleaned['title'], cleaned['author'], cleaned['price'], cleaned['quantity'])
            )
            conn.commit()
            conn.close()

            flash(f"Book '{cleaned['title']}' was added successfully!", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Database error while adding book: {str(e)}", 'danger')
            return render_template('add_book.html', form_data=request.form), 500

    return render_template('add_book.html', form_data={})


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """
    Edit existing book details.
    GET: Render edit form pre-filled with book data.
    POST: Validate inputs and update book record.
    """
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if book is None:
        conn.close()
        flash(f"Book with ID #{book_id} was not found.", 'warning')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')

        is_valid, errors, cleaned = validate_book_data(title, author, price, quantity)

        if not is_valid:
            conn.close()
            for error in errors:
                flash(error, 'danger')
            # Render with the invalid input so user can correct it
            return render_template('edit_book.html', book=book, form_data=request.form), 400

        try:
            conn.execute(
                '''UPDATE books
                   SET title = ?, author = ?, price = ?, quantity = ?
                   WHERE id = ?''',
                (cleaned['title'], cleaned['author'], cleaned['price'], cleaned['quantity'], book_id)
            )
            conn.commit()
            conn.close()

            flash(f"Book #{book_id} ('{cleaned['title']}') was updated successfully!", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            conn.close()
            flash(f"Database error while updating book: {str(e)}", 'danger')
            return render_template('edit_book.html', book=book, form_data=request.form), 500

    conn.close()
    return render_template('edit_book.html', book=book, form_data={})


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book from the inventory by its ID.
    Only allows POST requests to prevent accidental deletion via GET web crawlers or URL navigation.
    """
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if book is None:
        conn.close()
        flash(f"Book with ID #{book_id} was not found or already deleted.", 'warning')
        return redirect(url_for('index'))

    try:
        book_title = book['title']
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()

        flash(f"Book '{book_title}' (ID #{book_id}) has been removed from inventory.", 'success')
    except Exception as e:
        conn.close()
        flash(f"Database error while deleting book: {str(e)}", 'danger')

    return redirect(url_for('index'))


# -------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# -------------------------------------------------------------
# Application Runner
# -------------------------------------------------------------

if __name__ == '__main__':
    # Support dynamic PORT for cloud platforms like Render / Railway
    port = int(os.environ.get('PORT', 5000))
    # Run development server
    app.run(host='0.0.0.0', port=port, debug=True)


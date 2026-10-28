import os
import unittest
import tempfile
import app as bookstore_app


class OnlineBookstoreTestCase(unittest.TestCase):
    """
    Automated test suite verifying the database setup, CRUD operations,
    input validations, and template responses for the Online Bookstore.
    """

    def setUp(self):
        # Create a temporary file to use as a fresh test database
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix='.db')
        bookstore_app.app.config['DATABASE'] = self.temp_db_path
        bookstore_app.app.config['TESTING'] = True
        bookstore_app.app.config['WTF_CSRF_ENABLED'] = False

        # Initialize the database and seed initial sample records
        bookstore_app.init_db()

        # Create test client
        self.client = bookstore_app.app.test_client()

    def tearDown(self):
        # Close and remove the temporary database after each test
        os.close(self.db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_database_initialization_and_sample_records(self):
        """Test that the database is created and sample books are seeded."""
        conn = bookstore_app.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM books")
        count = cursor.fetchone()['count']
        conn.close()
        # Initial sample books should be at least 6
        self.assertGreaterEqual(count, 6)

    def test_index_page_displays_books_and_stats(self):
        """Test that the home page displays book information and inventory metrics."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')

        # Check for core headers and sample book titles
        self.assertIn("Book Inventory Dashboard", content)
        self.assertIn("To Kill a Mockingbird", content)
        self.assertIn("Harper Lee", content)
        self.assertIn("Clean Code", content)
        self.assertIn("Inventory Valuation", content)

    def test_add_book_get(self):
        """Test GET request to /add loads the book creation form."""
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Add New Book", response.data.decode('utf-8'))

    def test_add_book_valid_post(self):
        """Test adding a new book with valid inputs successfully saves to DB."""
        new_book_data = {
            'title': 'Design Patterns: Elements of Reusable Object-Oriented Software',
            'author': 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
            'price': '45.50',
            'quantity': '10'
        }
        response = self.client.post('/add', data=new_book_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("Design Patterns", content)
        self.assertIn("was added successfully", content)

        # Verify record directly in database
        conn = bookstore_app.get_db_connection()
        book = conn.execute(
            "SELECT * FROM books WHERE title LIKE ?",
            ('%Design Patterns%',)
        ).fetchone()
        conn.close()
        self.assertIsNotNone(book)
        self.assertEqual(book['price'], 45.50)
        self.assertEqual(book['quantity'], 10)

    def test_add_book_validation_failures(self):
        """Test form validations: empty title, empty author, invalid price, negative quantity."""
        # 1. Missing title
        res = self.client.post('/add', data={
            'title': '',
            'author': 'Valid Author',
            'price': '19.99',
            'quantity': '5'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Book title is required", res.data.decode('utf-8'))

        # 2. Missing author
        res = self.client.post('/add', data={
            'title': 'Valid Title',
            'author': '',
            'price': '19.99',
            'quantity': '5'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Author name is required", res.data.decode('utf-8'))

        # 3. Negative price
        res = self.client.post('/add', data={
            'title': 'Valid Title',
            'author': 'Valid Author',
            'price': '-5.00',
            'quantity': '5'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Price must be a positive number", res.data.decode('utf-8'))

        # 4. Non-numeric price
        res = self.client.post('/add', data={
            'title': 'Valid Title',
            'author': 'Valid Author',
            'price': 'free',
            'quantity': '5'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Price must be a valid numeric value", res.data.decode('utf-8'))

        # 5. Negative quantity
        res = self.client.post('/add', data={
            'title': 'Valid Title',
            'author': 'Valid Author',
            'price': '15.00',
            'quantity': '-2'
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Quantity cannot be negative", res.data.decode('utf-8'))

    def test_edit_book_get_and_post(self):
        """Test retrieving and updating an existing book."""
        # Book ID 1 is 'To Kill a Mockingbird'
        response = self.client.get('/edit/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("To Kill a Mockingbird", response.data.decode('utf-8'))

        # Update the book price and quantity
        updated_data = {
            'title': 'To Kill a Mockingbird (Special Anniversary Edition)',
            'author': 'Harper Lee',
            'price': '18.99',
            'quantity': '25'
        }
        post_response = self.client.post('/edit/1', data=updated_data, follow_redirects=True)
        self.assertEqual(post_response.status_code, 200)
        content = post_response.data.decode('utf-8')
        self.assertIn("Special Anniversary Edition", content)
        self.assertIn("was updated successfully", content)

        # Verify change in SQLite database
        conn = bookstore_app.get_db_connection()
        book = conn.execute("SELECT * FROM books WHERE id = 1").fetchone()
        conn.close()
        self.assertEqual(book['price'], 18.99)
        self.assertEqual(book['quantity'], 25)

    def test_edit_book_invalid_id(self):
        """Test editing a non-existent book returns a redirect with flash message."""
        response = self.client.get('/edit/99999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("was not found", response.data.decode('utf-8'))

    def test_delete_book(self):
        """Test deleting a book removes it from the inventory."""
        # Delete book ID 2 ('1984')
        response = self.client.post('/delete/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("has been removed from inventory", content)

        # Verify book ID 2 no longer exists in database
        conn = bookstore_app.get_db_connection()
        book = conn.execute("SELECT * FROM books WHERE id = 2").fetchone()
        conn.close()
        self.assertIsNone(book)

    def test_search_functionality(self):
        """Test search query filters books appropriately."""
        response = self.client.get('/?q=Orwell')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("1984", content)
        # Another book that doesn't match should not be in filtered results
        self.assertNotIn("The Great Gatsby", content)


if __name__ == '__main__':
    unittest.main()


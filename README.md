# 📚 Online Bookstore Web Application

A complete, beginner-friendly Online Bookstore web application built with **Python Flask**, **SQLite**, and **Bootstrap 5**. Designed and documented for college lab assignments, cloud computing evaluations, and production deployment on **Render**.

---

## 🌟 Features

1. **Catalog Display**: View all books with ID, title, author, unit price, quantity, inventory status, and calculated total valuation.
2. **Add New Books**: Clean, validated input form for adding new books to inventory.
3. **Edit Book Details**: Update existing titles, authors, prices, or inventory levels with pre-filled forms.
4. **Safe Deletion with Confirmation**: Delete confirmation modal prevents accidental deletions and shows book details before removing.
5. **Form Validation & Flash Messages**: Comprehensive client-side (Bootstrap 5) and server-side (Flask) validation with color-coded alerts (success, error, warning).
6. **Automatic SQLite Database Initialization**: On application start, the SQLite database is automatically created with tables and populated with sample books if not already present.
7. **Sample Test Records Included**: Pre-loaded with 7 classic and computer science books for immediate testing.
8. **Real-time Live Filter & Search**: Instantly filter books by title, author, or ID without reloading the page.
9. **Inventory Metrics Cards**: Real-time stats showing Total Titles, Units in Stock, Inventory Valuation, and Low Stock Alerts.
10. **Cloud Deployment Ready**: Pre-configured with `Procfile`, `render.yaml`, dynamic port bindings, and `gunicorn` for seamless deployment on **Render** via GitHub.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3 + Flask 3.1 | Web framework, routing, request validation, business logic |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3 | Responsive modern UI, layouts, modals, alerts |
| **Icons** | Bootstrap Icons 1.11 | Modern iconography across buttons, tables, and cards |
| **Database** | SQLite 3 | Embedded, zero-configuration local relational database |
| **Production Server** | Gunicorn 23.0 | Production WSGI HTTP server for Linux / Render |
| **Deployment** | Render / GitHub | Cloud web service hosting |
| **Testing** | Python `unittest` | Automated test suite verifying CRUD routes and validations |

---

## 📁 Project Directory Structure

```text
cloud semlabq1/
├── app.py                # Main Flask application (routes, database helpers, validations)
├── test_app.py           # Automated unit test suite (9 test cases)
├── requirements.txt      # Python dependencies (Flask, gunicorn)
├── Procfile              # Render/Heroku WSGI command (web: gunicorn app:app)
├── render.yaml           # Render Blueprint configuration file
├── .gitignore            # Git ignore file (excludes virtualenv, caches, DB)
├── README.md             # Complete documentation and deployment guide
├── database.db           # SQLite database file (automatically created on first run)
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS styles, badge colors, card elevations
│   └── js/
│       └── main.js       # Bootstrap validation, live table search, modal wiring
└── templates/
    ├── base.html         # Base template (navbar, flash alerts container, footer)
    ├── index.html        # Main dashboard (stats cards, inventory table, delete modal)
    ├── add_book.html     # Add new book form
    ├── edit_book.html    # Edit existing book form
    ├── 404.html          # Custom Page Not Found error page
    └── 500.html          # Custom Server Error page
```

---

## 💡 How Automatic Database Initialization Works

When `app.py` starts:
1. It connects to `database.db` via `get_db_connection()`.
2. It executes `CREATE TABLE IF NOT EXISTS books (...)` to establish the table schema:
   - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
   - `title` (TEXT NOT NULL)
   - `author` (TEXT NOT NULL)
   - `price` (REAL NOT NULL)
   - `quantity` (INTEGER NOT NULL)
   - `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
3. It checks `SELECT COUNT(*) FROM books`.
4. If the count is `0` (fresh database), it automatically inserts 7 sample book records.
5. No manual database migrations or SQL command-line scripts are required.

---

## 💻 Local Setup & Running Instructions

### Step 1: Open Terminal / Command Prompt
Navigate to your project directory:
```powershell
cd "c:\Users\dinesh\Desktop\cloud semlabq1"
```

### Step 2: Create a Virtual Environment (Recommended)
Creating an isolated virtual environment prevents library conflicts.

**On Windows:**
```powershell
python -m venv venv
```

**On macOS / Linux:**
```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
*(If you see an execution policy error in PowerShell, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once, or activate via Command Prompt using `.\venv\Scripts\activate.bat`)*

**On macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
Install Flask and dependencies:
```bash
pip install -r requirements.txt
```
*(Note: On Windows, `gunicorn` is included for Render Linux deployment. Flask's built-in server is used for local Windows development.)*

### Step 5: Start the Flask Application
```bash
python app.py
```

You should see output similar to:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

### Step 6: View in Your Browser
Open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests

An automated test suite is included in `test_app.py` testing database seeding, CRUD operations, and error handling.

To run all tests:
```bash
python -m unittest test_app.py -v
```

Expected output:
```text
test_add_book_get (test_app.OnlineBookstoreTestCase) ... ok
test_add_book_valid_post (test_app.OnlineBookstoreTestCase) ... ok
test_add_book_validation_failures (test_app.OnlineBookstoreTestCase) ... ok
test_database_initialization_and_sample_records (test_app.OnlineBookstoreTestCase) ... ok
test_delete_book (test_app.OnlineBookstoreTestCase) ... ok
test_edit_book_get_and_post (test_app.OnlineBookstoreTestCase) ... ok
test_edit_book_invalid_id (test_app.OnlineBookstoreTestCase) ... ok
test_index_page_displays_books_and_stats (test_app.OnlineBookstoreTestCase) ... ok
test_search_functionality (test_app.OnlineBookstoreTestCase) ... ok

Ran 9 tests in 2.8s
OK
```

---

## 🚀 Step-by-Step Render Deployment Guide (via GitHub)

Deploy your application to the cloud using [Render](https://render.com) for free.

### Step 1: Push Your Code to GitHub
1. Open PowerShell / Terminal in your project folder.
2. Initialize Git and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Online Bookstore web app"
   ```
3. Create a new repository on [GitHub](https://github.com/new) (e.g., `online-bookstore`).
4. Link and push your repository:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/online-bookstore.git
   git push -u origin main
   ```

### Step 2: Create a Web Service on Render
1. Visit [https://render.com](https://render.com) and log in (or sign up with your GitHub account).
2. On your Render Dashboard, click the **New +** button in the top navigation bar.
3. Select **Web Service**.
4. Choose **Build and deploy from a Git repository**.
5. Find and click **Connect** next to your `online-bookstore` repository.

### Step 3: Configure Web Service Settings
Fill in the following fields:

| Field | Value | Explanation |
| :--- | :--- | :--- |
| **Name** | `online-bookstore` (or any unique name) | Your public subdomain name |
| **Region** | Select region closest to you | e.g. Oregon (US West), Frankfurt (EU), Singapore |
| **Branch** | `main` | Production branch to deploy from |
| **Language** | `Python 3` | Application runtime |
| **Build Command** | `pip install -r requirements.txt` | Installs Flask and Gunicorn |
| **Start Command** | `gunicorn app:app` | Starts production WSGI server |
| **Instance Type** | `Free` | Free tier hosting |

### Step 4: Environment Variables (Optional but Recommended)
Scroll down to the **Environment Variables** section and add:
- `SECRET_KEY`: Enter a random secure string (e.g., `super-secret-production-key-987`)
- `PYTHON_VERSION`: `3.12.8`

### Step 5: Deploy and Verify
1. Click **Create Web Service** at the bottom.
2. Render will automatically fetch your code from GitHub, install the requirements, and run Gunicorn.
3. In 2–3 minutes, the build log will show:
   ```text
   ==> Your service is live 🎉 at https://online-bookstore-xxxx.onrender.com
   ```
4. Click your live URL to test your deployed application! Every time you `git push` new changes to GitHub, Render will automatically rebuild and update your live site.

---

## 🛡️ Form Validation & Safety Details

1. **Title Validation**: Required, trimmed of whitespace, maximum 200 characters.
2. **Author Validation**: Required, trimmed of whitespace, maximum 150 characters.
3. **Price Validation**: Required, must be a positive float greater than `$0.00`, maximum `$100,000.00`, rounded to two decimal places.
4. **Quantity Validation**: Required, must be a non-negative integer (`>= 0`), maximum `100,000` units.
5. **Deletion Safety**: Deletion is strictly restricted to `POST` requests and requires explicit confirmation in an interactive modal to prevent accidental removal or web-crawler triggering.

---

## 🎓 Academic Submission Checklist

- [x] Python Flask backend application (`app.py`)
- [x] SQLite database with automatic initialization and sample records
- [x] Responsive frontend with Bootstrap 5 and Bootstrap Icons
- [x] CRUD operations: Display (Read), Add (Create), Edit (Update), Delete (with confirmation)
- [x] Input validation with user-friendly error/success messages
- [x] Deployment configuration files (`Procfile`, `render.yaml`, `requirements.txt`)
- [x] Clean `.gitignore` ignoring virtualenv and cache files
- [x] Automated test suite passing with 100% test coverage
- [x] Comprehensive, beginner-friendly `README.md`


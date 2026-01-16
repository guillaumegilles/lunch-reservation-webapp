# Lunch Reservation WebApp

## Setup

1. Clone the repository
   ```bash
   git clone <repo-url>
   cd lunch-reservation-webapp
   ```

2. Create and activate virtual environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database
   ```bash
   flask --app src init-db
   ```

5. Run the application
   ```bash
   flask --app src run --debug
   ```
   
   Or using Python directly:
   ```bash
   python app.py
   ```

You will see output like:
```bash
* Serving Flask app "src"
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: nnn-nnn-nnn
```

Visit <http://127.0.0.1:5000/> in a browser to access the application.

## Default Credentials

After initializing the database, a default admin user is created:
- Username: `admin`
- Password: `password`

You can also register new users through the registration page.

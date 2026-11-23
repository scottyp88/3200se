# US Military Rifles — Authentication

This project adds account registration, login, and sessions to my rifle database from project4. Users can create an account and log in to view, search, add, edit, and delete rifle records. All logged-in users have the same access to the rifle data.

## Running the project

Use Python 3 and run these commands from the project5 folder.

### Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

### Set up the database

The application uses `app.db` in the current working directory. The included database has rifle records and an empty users table; accounts created during testing were removed before submission. You can use it directly.

To rebuild the database instead, move the existing `app.db` out of the project folder first, then create the tables and load the starting rifle records with:

```bash
sqlite3 app.db < schema.sql
sqlite3 app.db < USrifles.sql
```

Run the rifle seed script once on a new database; its explicit IDs will conflict if those records already exist. `schema.sql` contains only table definitions. `USrifles.sql` contains the starting rifle data and no accounts. Create an account through the registration form.

If the SQLite command-line tool is unavailable, open or create `app.db` in DB Browser for SQLite, execute `schema.sql` followed by `USrifles.sql`, and write the changes.

### Start the backend

With the Python environment activated:

```bash
python3 -m flask --app app run --host 127.0.0.1 --port 5001
```

### Start the frontend

In a second terminal, from the project5 folder:

```bash
python3 -m http.server 5500 --bind 127.0.0.1
```

Open [the account page](http://127.0.0.1:5500/index.html). Use `127.0.0.1` consistently: the API allows the frontend origin `http://127.0.0.1:5500` with credentials, and the JavaScript calls the API at `http://127.0.0.1:5001`.

## Using the application

1. Create an account with a first name, last name, email, and password. The page displays an alert with the result and clears the registration form after success.
2. Log in with the account's email and password. Successful login opens `rifles.html`; failed login displays an error alert.
3. View or search the rifle records, or use the rifle form to add and edit records. Each record also has a delete control.
4. Use Logout to end the session and return to the account page.

The rifle page starts hidden and checks the session before showing its controls or loading records. Each rifle API endpoint also checks the session. If a rifle request receives 401, the client hides the interface and returns to login. Application data is sent through Ajax requests using `fetch()`.

## Resources

### User

| Attribute | SQLite type | Description |
| --- | --- | --- |
| `id` | INTEGER | Automatically assigned primary key |
| `fname` | TEXT | First name |
| `lname` | TEXT | Last name |
| `email` | TEXT | Required unique email address |
| `pass` | TEXT | Salted password hash, not the original password |

Registration JSON uses `fname`, `lname`, `email`, and `pswrd`. Login JSON uses `email` and `pswrd`. The server hashes the submitted `pswrd` before storing it in `pass`. Login and current-user responses include `[id, fname, lname, email]` and exclude the hash.

### Rifle

| Attribute | SQLite type | Description |
| --- | --- | --- |
| `id` | INTEGER | Automatically assigned primary key |
| `name` | TEXT | Rifle name |
| `cartridge` | TEXT | Cartridge used |
| `action_type` | TEXT | Action type |
| `barrel_length_in` | TEXT | Barrel length in inches |
| `adoption_year` | TEXT | Year adopted |
| `weight_lb` | TEXT | Weight in pounds |
| `standard_capacity` | TEXT | Standard magazine or feed capacity |
| `adoption_branch` | TEXT | Adopting military branch |

Rifle values other than the ID are stored as text to support values such as `unknown`. Rifle JSON responses use the column order shown above. Creating or updating a rifle requires the eight attributes other than `id` in a JSON object.

## Database schema

Database operations are encapsulated in the `DATABASE` class in `app.py`. User input is passed to parameterized SQLite queries.

```sql
CREATE TABLE IF NOT EXISTS rifles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cartridge TEXT NOT NULL DEFAULT 'unknown',
    action_type TEXT NOT NULL DEFAULT 'unknown',
    barrel_length_in TEXT NOT NULL DEFAULT 'unknown',
    adoption_year TEXT NOT NULL DEFAULT 'unknown',
    weight_lb TEXT NOT NULL DEFAULT 'unknown',
    standard_capacity TEXT NOT NULL DEFAULT 'unknown',
    adoption_branch TEXT NOT NULL DEFAULT 'unknown'
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    pass TEXT NOT NULL
);
```

## REST endpoints

The API runs at `http://127.0.0.1:5001`. Request bodies containing data use `Content-Type: application/json`.

| Name | Method | Path | Session required | Response |
| --- | --- | --- | --- | --- |
| Create account | POST | `/users` | No | 201 with the new user ID; 400 for missing or invalid fields; 409 for an existing email |
| Log in | POST | `/login` | No | 200 with a message, basic user data, and a session cookie; 400 for invalid fields; 401 for incorrect credentials |
| Check current user | GET | `/users` | Yes | 200 with a message and basic user data; 401 if the session or user is missing |
| Log out | DELETE | `/sessions/current` | Yes | 200 with a message and a cleared cookie; 401 if no valid session exists |
| Retrieve rifle collection | GET | `/rifles` | Yes | 200 with an array of rifle rows |
| Retrieve rifle member | GET | `/rifles/<int:item>` | Yes | 200 with a rifle row; 404 if missing |
| Create rifle member | POST | `/rifles` | Yes | 201 with the new rifle ID; 400 for missing or invalid data |
| Replace rifle member | PUT | `/rifles/<int:item>` | Yes | 200 with the updated rifle row; 400 for missing or invalid data; 404 if missing |
| Delete rifle member | DELETE | `/rifles/<int:item>` | Yes | 204 with no response body; 404 if missing |

All rifle operations return 401 before accessing the resource if the session is missing or invalid. Flask provides OPTIONS responses for preflight requests. Unknown paths return 404, unsupported methods return 405, malformed JSON returns 400, and JSON endpoints reject an incorrect content type with 415.

Registration checks required fields for string types and empty values and checks the database for an existing email. The database also enforces email uniqueness. The form uses an email input for browser format validation. The current registration constraint-error handler reports an integrity violation as an existing email.

## Password hashing

The application uses Werkzeug's `generate_password_hash()` when registering and `check_password_hash()` when logging in. Werkzeug is installed as a Flask dependency.

The defaults verified in the development environment with Werkzeug 3.1.9 are:

- Method: scrypt
- Cost parameter `N`: 32768
- Block size parameter `r`: 8
- Parallelization parameter `p`: 1
- Random salt length: 16 characters

The stored value includes the method, parameters, salt, and hash. The original password is not stored in the database or session. Verification uses the stored hash for the account found by email. These are library defaults; check the installed Werkzeug version if upgrading dependencies.

## Sessions and cookies

Sessions are held in a Python dictionary in server memory. On successful login, `secrets.token_urlsafe(32)` generates a session ID using 32 random bytes. The dictionary associates that ID with only the authenticated user's database ID.

The browser receives the ID in a `session_id` cookie with HttpOnly, SameSite=Lax, and path `/`. Cookie-based Ajax requests include `credentials: "include"`. Logout removes the dictionary entry and expires the cookie. Restarting the backend clears all sessions and requires users to log in again.

The local development servers use HTTP. The cookie is not marked Secure for that setup; an HTTPS deployment should use Secure cookies. This basic in-memory store is intended for the assignment's single-process server.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Flask routes, database class, sessions, and authorization |
| `app.db` | Ready-to-use SQLite database with rifle records and no submitted accounts |
| `index.html` | Login and registration forms |
| `auth.js` | Registration and login requests and feedback |
| `rifles.html` | Protected rifle interface |
| `script.js` | Session check, rifle requests, and logout |
| `styles.css` | Shared styling and page backgrounds |
| `assets/flag-background-blue.png` | Generated blue flag background |
| `schema.sql` | Both table definitions, without account data |
| `USrifles.sql` | Rifle schema and starting rifle records |
| `requirements.txt` | Python dependencies |

The frontend uses plain HTML, CSS, and JavaScript without third-party JavaScript or CSS libraries.

## Validation

77 backend checks passed using Flask's test client and a temporary copy of the database. They covered registration, duplicate emails, stored password hashes, invalid input, valid and invalid login, cookie flags, current-user lookup, all five rifle operations, unauthenticated requests, missing records, CORS headers and preflight, logout, and rejection of old sessions.

Those checks did not change the working database. Browser behavior, including the registration form reset, should also be verified through the running frontend.

# US Military Rifles

## Resources

Rifle

Attributes:

- id (integer, primary key)
- name (text)
- cartridge (text)
- action_type (text)
- barrel_length_in (text)
- adoption_year (text)
- weight_lb (text)
- standard_capacity (text)
- adoption_branch (text)

User

Attributes:

- id (integer, primary key)
- fname (text)
- lname (text)
- email (text, unique)
- pass (text, password hash)

## Schema

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

## REST Endpoints

| Name | Method | Path |
| --- | --- | --- |
| Retrieve rifle collection | GET | `/rifles` |
| Retrieve rifle member | GET | `/rifles/<id>` |
| Create rifle member | POST | `/rifles` |
| Update rifle member | PUT | `/rifles/<id>` |
| Delete rifle member | DELETE | `/rifles/<id>` |
| Create user | POST | `/users` |
| Log in | POST | `/login` |
| Check current user | GET | `/users` |
| Log out | DELETE | `/sessions/current` |

All rifle endpoints require a valid session and return 401 if the user is not authenticated. All authenticated users have the same access.

Registration accepts `fname`, `lname`, `email`, and `pswrd` as JSON. It returns 201 with the new user ID, 400 for invalid fields, or 409 for an existing email.

Login accepts `email` and `pswrd` as JSON. It returns 200 with basic user information and a session cookie, 400 for invalid fields, or 401 for incorrect credentials. User information does not include the password hash.

## Password Hashing

Passwords are hashed with Werkzeug's `generate_password_hash()` and verified with `check_password_hash()`. The original password is not stored.

The defaults used in development with Werkzeug 3.1.9 are scrypt with `N=32768`, `r=8`, `p=1`, and a random salt length of 16 characters. The stored hash includes the method, parameters, and salt.

## Sessions

A dictionary in server memory stores each session ID and its user ID. Session IDs are generated with `secrets.token_urlsafe(32)` and sent in an HttpOnly, SameSite=Lax cookie named `session_id`. Logout removes the session and clears the cookie. Restarting the server clears all sessions.

## Running the Application

Run these commands from the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask --app app run --host 127.0.0.1 --port 5001
```

In a second terminal, from the same folder:

```bash
python3 -m http.server 5500 --bind 127.0.0.1
```

Open [index.html](http://127.0.0.1:5500/index.html). Use `127.0.0.1` for both servers because CORS allows `http://127.0.0.1:5500` with credentials.

The included `app.db` has rifle data and no accounts. Create an account through the registration form. To rebuild a database, move the existing `app.db` out of the folder first, then run:

```bash
sqlite3 app.db < schema.sql
sqlite3 app.db < USrifles.sql
```

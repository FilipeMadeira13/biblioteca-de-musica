# 🎵 Music Library REST API

A modern REST API for managing a music library, built with FastAPI and SQLAlchemy. The project is organized into `app/` modules with separate models, schemas, routers, authentication, and database configuration.

## ✨ Key Features

- **Full CRUD**: Create, Read, Update, and Delete operations for Artists, Genres, Albums, and Users
- **Authentication**: JWT auth with `/auth/login` and protected user endpoints
- **Complex Relationships**: One-to-Many and Many-to-Many support
- **Data Validation**: Automatic request validation with Pydantic 2.x
- **Error Handling**: Clear HTTP responses with descriptive error messages
- **Interactive Docs**: Built-in Swagger UI for easy testing
- **Advanced Type Hints**: Fully typed code using SQLAlchemy 2.0 `Mapped`
- **Modern SQLAlchemy**: Uses `mapped_column` and `Mapped` for better type safety
- **Environment Validation**: Required `.env` variables with explicit runtime checks

See `requirements.txt` for the full dependency list.

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 12+ installed and running (the local setup below uses `127.0.0.1:5432`)
- PostgreSQL client tools (`psql` and `createdb`) available in your terminal
- pip

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/FilipeMadeira13/biblioteca-de-musica.git
cd biblioteca-de-musica
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify PostgreSQL access

The examples below use the PostgreSQL user `postgres` for local development. If you use another database user, replace `postgres` consistently in the commands and `DATABASE_URL`.

In your operating system terminal, test the connection to the existing maintenance database named `postgres`:

```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres -W
```

Enter the PostgreSQL user's password when prompted. This is separate from your operating system password and from users registered through the API. The password is hidden while you type.

After a successful connection, run these commands inside `psql` to confirm the current database user and return to your operating system terminal:

```text
SELECT current_user;
\q
```

If authentication fails, resolve it before continuing; see [PostgreSQL authentication errors](#postgresql-authentication-errors).

### 5. Create the application database

The application needs an existing database named `music_library`. Run this command in your operating system terminal to create it, with `postgres` as its owner:

```bash
createdb -h 127.0.0.1 -p 5432 -U postgres -W music_library
```

Enter the same PostgreSQL password used in step 4. A successful `createdb` command normally finishes without printing a message. The database user needs permission to create databases (`CREATEDB` or superuser privileges); otherwise, ask your database administrator to create it with your application user as owner. See the [PostgreSQL `createdb` reference](https://www.postgresql.org/docs/16/app-createdb.html).

If `music_library` already exists, skip creation. Verify access to the application database:

```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d music_library -W
```

Once connected, enter `\q` to return to your operating system terminal.

`Base.metadata.create_all(bind=engine)` in `app/main.py` creates missing model tables inside an existing database. It does not create the PostgreSQL database itself.

### 6. Configure environment variables

Create a `.env` file in the project root, next to `README.md`:

```env
DATABASE_URL=postgresql://postgres:YOUR_URL_ENCODED_PASSWORD@127.0.0.1:5432/music_library
SECRET_KEY=YOUR_RANDOM_SECRET_KEY
```

Replace both placeholders with your own values. Use the same database user, password, host, port, and database name verified above. The example does not create a user or set a PostgreSQL password. Keep your real credentials in your local `.env` file.

Special characters in the password must be URL encoded. For example, the fictitious password `demo@123` becomes `demo%40123` in `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:demo%40123@127.0.0.1:5432/music_library
```

To encode your password, this command prompts for it with hidden input and prints the encoded value:

```bash
python -c "from getpass import getpass; from urllib.parse import quote; print(quote(getpass('PostgreSQL password: '), safe=''))"
```

Encode only the password, once, and use the resulting value in `DATABASE_URL`. Enter the original password in `psql` and `createdb`. See [SQLAlchemy's password encoding guide](https://docs.sqlalchemy.org/en/20/core/engines.html#escaping-special-characters-such-as-at-signs-in-passwords).

Generate a random `SECRET_KEY` and copy the output into `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

`app/config.py` loads `.env` using `load_dotenv()`. Variables already defined in the process environment take priority over the file, as described in the [python-dotenv documentation](https://bbc2.github.io/python-dotenv/#getting-started).

### 7. Run the application

From the project root, with the virtual environment active:

```bash
uvicorn app.main:app --reload
```

Wait for `Application startup complete.` before opening `http://127.0.0.1:8000/docs`. The initial `Uvicorn running on ...` message alone does not confirm that the application loaded successfully.

After editing `.env`, stop Uvicorn with `Ctrl+C` and start it again to reload the configuration.

## 📚 API Documentation

Interactive documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Architecture and Structure

The project is organized under the `app/` directory:

```
app/
├── config.py          # Environment variable loading
├── database.py        # SQLAlchemy engine and session configuration
├── main.py            # FastAPI application entry point
├── security.py        # Password hashing and JWT helpers
├── dependencies.py    # Dependency helpers for protected endpoints
├── models/            # SQLAlchemy models
│   ├── album.py
│   ├── artist.py
│   ├── genre.py
│   ├── album_genre.py
│   └── user.py
├── routers/           # FastAPI routers by resource
│   ├── album.py
│   ├── artist.py
│   ├── genre.py
│   ├── user.py
│   └── auth.py
└── schemas/           # Pydantic schemas by resource
    ├── album.py
    ├── artist.py
    ├── genre.py
    ├── token.py
    └── user.py
```

### Data Models

All models use SQLAlchemy 2.0 with `Mapped` type hints.

#### Artist
```python
class Artist(Base):
    id: Mapped[int]
    name: Mapped[str]
    country_of_origin: Mapped[str]
    year_formed: Mapped[int]
    albums: Mapped[list["Album"]]
```

#### Genre
```python
class Genre(Base):
    id: Mapped[int]
    name: Mapped[str]
    albums: Mapped[list["Album"]]
```

#### Album
```python
class Album(Base):
    id: Mapped[int]
    title: Mapped[str]
    artist_id: Mapped[int]
    artist: Mapped["Artist"]
    genres: Mapped[list["Genre"]]
```

#### User
```python
class User(Base):
    id: Mapped[int]
    name: Mapped[str]
    password_hash: Mapped[str]
```

> Albums and Genres are connected via a many-to-many relationship through the `album_genre` association table.

### Database Configuration

SQLAlchemy configuration is in `app/database.py`:

```python
from app.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**Features:**
- Required `DATABASE_URL` validation via `.env`
- Database session management with dependency cleanup
- Compatible with SQLAlchemy-supported engines

## 🔐 Authentication

The project includes JWT-based authentication using `python-jose` and `bcrypt`.

- `POST /auth/login` accepts OAuth2 password form data and returns an access token
- Protected user endpoints require `Authorization: Bearer <token>`

## 🔌 Available Endpoints

### Authentication
```
POST /auth/login            # Login and receive JWT token
```

### Users
```
POST   /users/              # Create a new user
GET    /users/              # List all users (requires auth)
GET    /users/me             # Get current authenticated user
```

### Artists
```
POST   /artists/            # Create a new artist
GET    /artists/            # List all artists
GET    /artists/{artist_id} # Get a specific artist
PUT    /artists/{artist_id} # Update an artist
DELETE /artists/{artist_id} # Delete an artist
```

### Genres
```
POST   /genres/             # Create a new genre
GET    /genres/             # List all genres
GET    /genres/{genre_id}   # Get a specific genre
PUT    /genres/{genre_id}   # Update a genre
DELETE /genres/{genre_id}   # Delete a genre
```

### Albums
```
POST   /albums/             # Create a new album
GET    /albums/             # List all albums
GET    /albums/{album_id}   # Get a specific album
PUT    /albums/{album_id}   # Update an album
DELETE /albums/{album_id}   # Delete an album
```

## 📝 Usage Examples

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name":"admin","password":"strongpassword"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=strongpassword"
```

### Create an Album
```bash
curl -X POST "http://localhost:8000/albums/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Abbey Road",
    "artist_id": 1,
    "genre_ids": [1, 2]
  }'
```

If `artist_id` or any `genre_id` does not exist, the API returns `404` with a descriptive error message.

## 🎯 Good Practices Implemented

✅ Clean code and clear project structure
✅ SQLAlchemy 2.0 typed models with `Mapped`
✅ Request validation using Pydantic 2.x
✅ JWT authentication and protected user endpoints
✅ Separate models, schemas, routers, and dependencies
✅ Complex relationship support with referential integrity
✅ Automatic Swagger documentation
✅ Dependency injection via FastAPI `Depends`
✅ Environment validation for required configuration
✅ Secure password hashing with `bcrypt`

## 🧪 Testing the API

Use Swagger UI at `http://localhost:8000/docs` to test endpoints interactively, or use Postman/Insomnia/`curl`.

## 🩹 Troubleshooting

### PostgreSQL authentication errors

If startup reports `password authentication failed for user "..."`, PostgreSQL was reached but rejected authentication. Test the same user and application database directly:

```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d music_library -W
```

Use your actual database user in place of `postgres`. Enter the original password when prompted. If the application database has not been created yet, use `-d postgres` to test authentication first.

Inside an authenticated `psql` session, `SELECT current_user;` shows the current connection's user and `\du` lists database roles (users and permission groups).

For PostgreSQL installed directly on Ubuntu, you can also list roles through local administrative access:

```bash
sudo -u postgres psql -p 5432 -d postgres -c '\du'
```

If `sudo` prompts for a password, enter your operating system user's password. This administrative connection does not verify the password used by your application's TCP connection. If you have no working database credentials, ask your database administrator to set up the database user and password before continuing.

If the manual TCP connection works but the application still fails, compare the credentials in `.env`, check password URL encoding, and check whether an existing `DATABASE_URL` environment variable is taking priority. On Linux/macOS, after stopping Uvicorn, you can test with the environment variable removed only for the new process:

```bash
env -u DATABASE_URL uvicorn app.main:app --reload
```

### `database "music_library" does not exist`

Create the database using [installation step 5](#5-create-the-application-database). If you intentionally use a different database, update `DATABASE_URL` to match it. Table creation during startup requires the database to exist first.

### Connection attempted through `@localhost/.s.PGSQL.5432`

Check the URL for an extra `@` before the host, such as `PASSWORD@@localhost`. PostgreSQL interprets a host beginning with `@` as a local socket address. If the first `@` belongs to the password, encode it as `%40`; if it was a typing mistake, remove it. Keep the `@` separator before the host. See [installation step 6](#6-configure-environment-variables).

### `permission denied for schema public` (PostgreSQL 15+)

On databases created with PostgreSQL 15+, regular users are no longer granted permission to create objects in the `public` schema by default. If `Base.metadata.create_all(bind=engine)` fails with this error, connect to the application database as its owner or an admin:

```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d music_library -W
```

Inside `psql`, replace `your_user` with the database user from `DATABASE_URL`. This grants access to the schema and permission to create tables in it:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO your_user;
```

## 📈 Possible Extensions

- Add role-based authorization and token refresh
- Implement pagination for GET endpoints
- Add search and filter functionality
- Write unit tests with pytest
- Add caching with Redis
- Implement structured logging
- Add CI/CD with GitHub Actions

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed by Filipe Madeira as a professional FastAPI + SQLAlchemy REST API example.

---

**⭐ If you found this project useful, please give it a star!**

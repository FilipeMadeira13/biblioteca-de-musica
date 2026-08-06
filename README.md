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
- PostgreSQL 12+
- pip

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/FilipeMadeira13/biblioteca-de-musica.git
cd biblioteca_de_musica
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

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/music_library
SECRET_KEY=your_secret_key_here
```

### 5. Run the application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

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

### `permission denied for schema public` (PostgreSQL 15+)

PostgreSQL 15+ no longer grants schema creation privileges automatically to regular users. If `Base.metadata.create_all(bind=engine)` fails with this error, connect with an admin user and grant access:

```sql
GRANT ALL ON SCHEMA public TO your_user;
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

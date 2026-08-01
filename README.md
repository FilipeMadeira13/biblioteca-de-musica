# 🎵 Music Library REST API

A modern REST API for managing a music library, built with FastAPI and SQLAlchemy. The project is organized into `app/` modules with separate models, schemas, routes, and database configuration.

## ✨ Key Features

- **Full CRUD**: Create, Read, Update, and Delete operations for Artists, Genres, and Albums
- **Complex Relationships**: One-to-Many and Many-to-Many support
- **Data Validation**: Automatic request validation with Pydantic 2.x
- **Error Handling**: Clear HTTP responses with descriptive error messages
- **Interactive Docs**: Built-in Swagger UI for easy testing
- **Advanced Type Hints**: Fully typed code using SQLAlchemy 2.0 `Mapped`
- **Modern SQLAlchemy**: Uses `mapped_column` and `Mapped` for better type safety
- **Database Validation**: Environment variable checks with explicit error handling

See `requirements.txt` for the full dependency list.

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or poetry

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

The code is organized under the `app/` directory:

```
app/
├── main.py            # FastAPI application entry point
├── database.py        # SQLAlchemy engine and session configuration
├── models/            # SQLAlchemy models
│   ├── album.py
│   ├── artist.py
│   ├── genre.py
│   ├── album_genre.py
│   └── user.py
├── routes/            # FastAPI routers by resource
│   ├── album.py
│   ├── artist.py
│   └── genre.py
└── schemas/           # Pydantic schemas by resource
    ├── album.py
    ├── artist.py
    ├── genre.py
    └── user.py
```

### Data Models

All models use SQLAlchemy 2.0 with `Mapped` type hints for maximum type safety.

#### Artist
```python
class Artist(Base):
    id: Mapped[int]           # Unique identifier
    name: Mapped[str]         # Artist name
    country_of_origin: Mapped[str]  # Country of origin
    year_formed: Mapped[int]   # Year formed
    albums: Mapped[list["Album"]]  # One-to-many relationship
```

#### Genre
```python
class Genre(Base):
    id: Mapped[int]           # Unique identifier
    name: Mapped[str]         # Genre name
    albums: Mapped[list["Album"]]  # Many-to-many relationship
```

#### Album
```python
class Album(Base):
    id: Mapped[int]            # Unique identifier
    title: Mapped[str]         # Album title
    artist_id: Mapped[int]     # Foreign key to artist
    artist: Mapped["Artist"]  # Many-to-one relationship
    genres: Mapped[list["Genre"]]  # Many-to-many relationship
```

> The relationship between Album and Genre is many-to-many, implemented through the `album_genre` association table.

### Database Configuration

SQLAlchemy configuration is in `app/database.py`:

```python
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**Features:**
- Required `DATABASE_URL` validation using `.env`
- Session management with cleanup via generator
- Support for any SQLAlchemy-compatible database (PostgreSQL, MySQL, SQLite, etc.)

## 🔌 Available Endpoints

### Artists
```
POST   /artists/              # Create a new artist
GET    /artists/              # List all artists
GET    /artists/{artist_id}   # Get a specific artist
PUT    /artists/{artist_id}   # Update an artist
DELETE /artists/{artist_id}   # Delete an artist
```

### Genres
```
POST   /genres/               # Create a new genre
GET    /genres/               # List all genres
GET    /genres/{genre_id}     # Get a specific genre
PUT    /genres/{genre_id}     # Update a genre
DELETE /genres/{genre_id}     # Delete a genre
```

### Albums
```
POST   /albums/               # Create a new album
GET    /albums/               # List all albums
GET    /albums/{album_id}     # Get a specific album
PUT    /albums/{album_id}     # Update an album
DELETE /albums/{album_id}     # Delete an album
```

## 📝 Usage Examples

### Create an Artist
```bash
curl -X POST "http://localhost:8000/artists/"   -H "Content-Type: application/json"   -d '{
    "name": "The Beatles",
    "country_of_origin": "United Kingdom",
    "year_formed": 1960
  }'
```

### Create a Genre
```bash
curl -X POST "http://localhost:8000/genres/"   -H "Content-Type: application/json"   -d '{
    "name": "Rock"
  }'
```

### Create an Album
A new album must reference an existing artist (`artist_id`) and optionally include a list of genre IDs (`genre_ids`):
```bash
curl -X POST "http://localhost:8000/albums/"   -H "Content-Type: application/json"   -d '{
    "title": "Abbey Road",
    "artist_id": 1,
    "genre_ids": [1, 2]
  }'
```

If `artist_id` or any `genre_id` does not exist, the API returns `404` with a clear error message.

## 🎯 Good Practices Implemented

✅ Clean code and clear structure
✅ Advanced type hints with SQLAlchemy 2.0
✅ Request validation using Pydantic 2.x
✅ Proper HTTP error handling
✅ Separate models, schemas, and routes
✅ Complex relationship support with referential integrity
✅ Automatic Swagger documentation
✅ Dependency injection via FastAPI `Depends`
✅ Environment validation for `DATABASE_URL`
✅ Class docstrings for model documentation
✅ `TYPE_CHECKING` imports to avoid circular references

## 🧪 Testing the API

Use Swagger UI at `http://localhost:8000/docs` to test endpoints interactively, or use Postman/Insomnia/`curl`.

## 🩹 Troubleshooting

### `permission denied for schema public` (PostgreSQL 15+)

PostgreSQL 15+ no longer grants schema creation privileges automatically to regular users. If `Base.metadata.create_all(bind=engine)` fails with this error, connect with an admin user (for example `postgres`) and grant access:

```sql
GRANT ALL ON SCHEMA public TO your_user;
```

## 📈 Possible Extensions

- Add authentication and authorization (JWT)
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

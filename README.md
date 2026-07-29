## PENDAHULUAN
FastAPI Boilerplate adalah template proyek untuk membangun REST API menggunakan FastAPI dengan struktur yang terorganisir dan scalable. Proyek ini menggunakan uv sebagai package manager dan virtual environment.

### Teknologi yang Digunakan
- FastAPI - Web framework modern untuk Python
- Pydantic - Data validation menggunakan Python type hints
- Uvicorn - ASGI server untuk menjalankan aplikasi
- uv - Package manager dan virtual environment

### Setup Virtual Environment
---
``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Inisialisasi Projek
---
```
uv init
```

### Install Dependencies
---
```
# Install FastAPI dengan standard features
uv add 'fastapi[standard]'

# Install dependencies lainnya
uv add pydantic
uv add uvicorn
uv add python-multipart  # Untuk file upload
uv add python-dotenv     # Untuk environment variables

# Install development dependencies
uv add --dev pytest
uv add --dev black
uv add --dev ruff
uv add --dev mypy
```

### Running Project
```
uv run fastapi dev
```


### Project Structure
---
```
/project
├── .venv/                 # Virtual environment
├── src/                   # Source code utama
│   ├── user/              # Module user
│   │   ├── __init__.py
│   │   ├── dependencies.py # Dependency injection
│   │   ├── models.py      # Pydantic models (DTO/Schema)
│   │   ├── router.py      # Route handlers
│   │   └── service.py     # Business logic
│   ├── product/           # Module product
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── service.py
│   └── __init__.py
├── tests/                 # Test files
│   ├── test_user.py
│   └── test_product.py
├── main.py               # Entry point aplikasi
├── pyproject.toml        # Konfigurasi projek
├── uv.lock              # Lock file untuk dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
└── README.md            # Dokumentasi projek
```
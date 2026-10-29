# 📚 Book Management REST API

A robust, production-grade RESTful API built with **Django** and **Django REST Framework (DRF)** for managing books, user profiles, and custom permissions. Designed with maintainability, security, and performance in mind, featuring a **100% test coverage suite with Pytest** and a **PostgreSQL** database.

---

## 🌟 Key Features

- **🔐 Custom Authentication & Authorization**: Token & Session authentication with role-based permissions (Regular Users, Book Owners, and Admin/Staff).
- **📖 Book Management**: Full CRUD capabilities for books with dynamic category assignment (*Biography*, *Fiction*, *Technology*, *History*, *Science*).
- **🛡️ Fine-Grained Permissions**: 
  - Read-only access for unauthenticated users.
  - Custom `IsOwnerOrReadOnly` object-level permissions ensuring only owners or staff can update/delete records.
- **👤 User Profile & Signals**: Automatic `UserProfile` generation via Django signals upon user registration, with support for bio and avatar image uploads.
- **🔍 Advanced Querying**: Built-in Filtering, Search (by title & author), Ordering, and Page-Number Pagination.
- **⚡ Fast & Optimized Test Suite**: High-speed test execution configured using lightweight `MD5PasswordHasher` and reusable Pytest factory fixtures.

---

## 🛠️ Tech Stack & Tools

- **Backend Framework**: Python, Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Testing**: Pytest, Pytest-Django, Pytest-Cov
- **Authentication**: REST Framework Token Authentication & Session Authentication
- **Deployment Platform**: Render

---

## 🧪 Testing & Code Quality

The project prioritizes quality assurance with a **100% test coverage** standard.

### Test Highlights:
- **35 Unit & Integration Tests** covering Authentication, CRUD, Permissions, Serializer Validations, Signals, Pagination, and Search.
- Custom `conftest.py` setup with reusable factory fixtures (`create_user`, `create_book`, `authenticated_client`).
- Payload optimizations using `PATCH` partial updates and dictionary unpacking.

### Running Tests locally:
```bash
# Run all tests with coverage report
pytest --cov=books

# Run tests with detailed verbosity
pytest -v
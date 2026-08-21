# 📚 Book Management REST API

A robust RESTful API built with Django REST Framework (DRF) featuring JWT Authentication, Object-level Permissions, Filtering, Pagination, Interactive API Documentation, and Automated Unit Tests.

## ✨ Features
* **User Authentication:** Registration, JWT Login, and Token Refreshing (`rest_framework_simplejwt`).
* **Book CRUD Operations:** Full management of book resources linked to specific owners.
* **Custom Permissions:** `IsOwnerOrReadOnly` ensures only book creators can update or delete their entries.
* **Filtering & Search:** Search books by title/description and filter by category/author (`django-filter`).
* **Pagination:** Standard page-number pagination for clean data delivery.
* **Interactive API Docs:** Built-in Swagger UI and ReDoc interface (`drf-spectacular`).
* **Automated Unit Testing:** Full coverage for auth and book CRUD endpoints using DRF `APITestCase`.

## 🛠️ Tech Stack
* Python 3.14 / Django 6.x
* Django REST Framework
* Simple JWT
* drf-spectacular (Swagger)
* SQLite (Development DB)

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Abdurohman-Dev/book_api_project.git](https://github.com/Abdurohman-Dev/book_api_project.git)
   cd book_api_project
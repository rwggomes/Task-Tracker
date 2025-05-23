
#  Task Tracker API

Task Tracker API built with **Django REST Framework**, supporting:

- CRUD operations for Tasks
- File uploads
- JWT-based Token Authentication
- PostgreSQL with Docker Compose

---

##  Getting Started

### Clone the repository

```bash
git clone <your-repo-url>
cd task-tracker-api
```

---

##  Running with Docker Compose

### Build and start the containers

```bash
docker-compose build
docker-compose up
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

##  Environment Variables (via docker-compose.yml)

- `POSTGRES_DB`: taskdb  
- `POSTGRES_USER`: taskuser  
- `POSTGRES_PASSWORD`: taskpassword  
- `POSTGRES_HOST`: db  

**Configured automatically via Docker Compose**.

---

##  Database

Uses **PostgreSQL** inside Docker.  
Run migrations after starting the containers:

```bash
docker-compose exec web python manage.py migrate
```

---

##  Authentication: Token (JWT)

Implemented using **djangorestframework-simplejwt**.

### Obtain token

```bash
curl -X POST -d "username=<your_username>&password=<your_password>" http://127.0.0.1:8000/api/token/
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### Refresh token

```bash
curl -X POST -d "refresh=<refresh_token>" http://127.0.0.1:8000/api/token/refresh/
```

---

##  Protected Endpoints

All CRUD operations `/api/tasks/` require **Bearer Token**.  
File upload `/api/upload/` is also **protected**.

Send the token in the **Authorization** header:

```bash
-H "Authorization: Bearer <access_token>"
```

---

##  Example: Create Task with file upload

```bash
curl -X POST   -H "Authorization: Bearer <access_token>"   -F "title=Test Task"   -F "status=pending"   -F "attachment=@/path/to/file.png"   http://127.0.0.1:8000/api/tasks/
```

---

##  Development without Docker

### Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run migrations:

```bash
python manage.py migrate
```

### Start server:

```bash
python manage.py runserver
```

---

## API Endpoints

| Method | URL | Description |
| --- | --- | --- |
| POST | `/api/token/` | Obtain JWT token |
| POST | `/api/token/refresh/` | Refresh JWT token |
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create task (with optional file) |
| GET | `/api/tasks/{id}/` | Retrieve task |
| PUT/PATCH | `/api/tasks/{id}/` | Update task |
| DELETE | `/api/tasks/{id}/` | Delete task |
| POST | `/api/upload/` | Upload file |

---

##  Technologies Used

- Python 3.13  
- Django 5.2  
- Django REST Framework  
- PostgreSQL  
- Docker Compose  
- JWT Authentication (`SimpleJWT`)


---

##  Example Using cURL:

```bash
curl -X POST   -H "Authorization: Bearer <access_token>"   -F "title=Test Task"   -F "description=Example upload"   -F "status=pending"   -F "attachment=@/path/to/file.png"   http://127.0.0.1:8000/api/tasks/
```

➡️ Response:

```json
{
  "id": 1,
  "title": "Test Task",
  "description": "Example upload",
  "status": "pending",
  "created_at": "2025-05-23T01:19:06.715850Z",
  "updated_at": "2025-05-23T01:19:06.715864Z",
  "attachment": "http://127.0.0.1:8000/media/attachments/file.png"
}
```

Access the file at the URL returned in the `attachment` field.



User Registration

You can create new users via the API.

Endpoint

POST /api/register/

Request (cURL)

```bash
curl -X POST   -H "Content-Type: application/json"   -d '{"username": "newuser", "password": "newpass123", "email": "newuser@example.com"}'   http://127.0.0.1:8000/api/register/
```

Response (HTTP 201 Created)

```json
{
  "username": "newuser",
  "email": "newuser@example.com"
}
```

Password is write-only and not returned for security reasons.

You can now authenticate with this user via the `/api/token/` endpoint.


Password Validation

This API uses Django's built-in password validators to ensure strong passwords during user registration.

Configuration

In `settings.py`:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

Implementation in Serializer

In `task_app/serializers.py`:

```python
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value
```

This ensures that weak passwords are rejected automatically.

Example Error Response:

```json
{
  "password": [
    "This password is too common."
  ]
}
```

Summary

- Enforces minimum length  
- Blocks common passwords  
- Prevents passwords similar to username  
- Rejects numeric-only passwords  

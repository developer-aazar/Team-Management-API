#  Team Management API

A secure team management REST API built with **FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication**.

The project focuses on authentication, role-based access control (RBAC), team membership management, and API security.

## 🚀 Features

* User signup & login
* JWT authentication
* Secure password hashing
* Team creation
* Team membership management
* Add / remove members
* Promote / demote members
* Leave team
* Owner / Admin / Member roles
* Role-based authorization
* Cross-team access protection
* Input validation
* Database transactions & migrations

## 🏗️ Architecture

```text
Client
  ↓
FastAPI Router
  ↓
Dependencies / Authorization
  ↓
Service Layer
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

## 🛠️ Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* JWT
* bcrypt

## 🔐 Security

The API was tested against common authorization and authentication issues, including:

* Unauthorized access
* Invalid & tampered JWTs
* IDOR / BOLA-style attacks
* Privilege escalation
* Cross-team access
* Role manipulation
* Owner protection

Authentication failures return `401`, while insufficient permissions return `403`.

## ⚙️ Run Locally

```bash
git clone https://github.com/developer-aazar/Team-Management-API
cd app

python -m venv venv
source venv/bin/activate

uv sync
```

Create a `.env` file with your PostgreSQL database URL and JWT configuration.

Then run:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🎯 V1

V1 focuses on building a **secure, structured backend API** with authentication, authorization, database integration, and practical security testing.

Future improvements may include refresh-token rotation, email verification, password reset, automated tests, rate limiting, audit logging, and CI/CD.

# Personalized Feed API

A **FastAPI** service that provides a personalized post feed based on user likes.  
It uses **content-based filtering** to determine user interests and serve relevant content.

---

## Live Demo

**First, seed the database:**

```bash
# macOS/Linux:
API_URL=https://humdov-interview.onrender.com python seed_data.py

# Windows PowerShell:
$env:API_URL="https://humdov-interview.onrender.com"; python seed_data.py

# Windows CMD:
set API_URL=https://humdov-interview.onrender.com && python seed_data.py

- **Base URL:** [https://humdov-interview.onrender.com](https://humdov-interview.onrender.com)
- **Interactive Docs (Swagger UI):** [https://humdov-interview.onrender.com/docs](https://humdov-interview.onrender.com/docs)
```

---

## Table of Contents

- [Features](#-features)
- [Getting Started](#-getting-started)
  - [Run Locally](#run-locally)
  - [Load Seed Data](#load-seed-data)
- [Endpoints](#-endpoints)
- [Recommendation Method](#-recommendation-method)
- [Error Handling](#-error-handling)
- [Testing](#-testing)

---

## Features

- **User and Post Management** – Create users and posts
- **Post Interaction** – Users can like posts
- **Personalized Feed** – Custom feed sorted by user interests
- **Robustness** – Comprehensive test coverage (success and error cases)

---

## Getting Started

### Run Locally

1. **Clone the repository** and navigate to its directory:

   ```bash
   git clone <your-repo-url>
   cd <repo-name>

   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   pip install fastapi uvicorn sqlalchemy databases aiosqlite requests pytest httpx psycopg2-binary
   ```

4. **Run the server**:

   ```bash
   uvicorn main:app --reload
   ```

   - API available at: [http://localhost:8000](http://localhost:8000)
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Load Seed Data

With the server running, open a new terminal and:

```bash
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
python seed_data.py
```

This creates **3 users** and **10 faith-based posts**, then assigns likes.

**Example users:**

- `Grace` → likes: _prayer, faith, worship_
- `John` → likes: _bible, sermon, outreach_
- `Hope` → likes: _hope, community_

---

## Endpoints

### Create a User

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice"}'
```

### Create a Post

```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "This is the content.",
    "tag": "tech"
  }'
```

### Like a Post

```bash
curl -X POST http://localhost:8000/users/1/like/5
```

### Get Personalized Feed

```bash
curl http://localhost:8000/users/1/feed
```

---

## Recommendation Method

- Uses **content-based filtering** with tags.
- Each post has a tag (e.g., `"prayer"`, `"sermon"`).
- Posts are scored `1` if their tag matches any user-liked tags, else `0`.
- Sorted by score, then by recency (ID order).

**Trade-offs & Assumptions:**

- Simple binary scoring.
- Considers explicit likes only.
- New users → reverse chronological order.
- Loads posts into memory (not optimized for scale).

---

## Error Handling

- Duplicate usernames → `400 Bad Request`
- Non-existent users or posts → `404 Not Found`
- Invalid request data → `422 Unprocessable Entity`

---

## Testing

Run tests:

```bash
pytest -v
```

Covers:

- User creation (success + duplicate errors)
- Feed generation
- Error handling (invalid users/posts)
- API validation

---

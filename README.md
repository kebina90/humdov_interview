````markdown
# Personalized Feed API

A simple FastAPI service that provides a personalized post feed based on user likes. It uses content-based filtering to determine user interests and serve relevant content.

---

## Features

- **User and Post Management:** Create users and posts.
- **Post Interaction:** Users can like posts.
- **Personalized Feed:** Get a custom feed for a user where posts are sorted based on their interests (determined by the tags of posts they've liked).
- **Robustness:** Includes comprehensive test coverage for success and error cases.

---

## How to Run Locally

1.  **Clone the repository** and navigate to its directory.
2.  **Set up a virtual environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy databases aiosqlite requests pytest httpx
    ```
4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    Interactive API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

---

## How to Load Seed Data

1.  **With the server running**, open a new terminal window.
2.  **Activate the virtual environment** in the new terminal:
    ```bash
    .\venv\Scripts\activate
    ```
3.  **Run the seeding script:**
    ```bash
    python seed_data.py
    ```
    This will create 3 users and 10 posts, then assign likes to all 3 users.

---

## Endpoints

### Create a User

```bash
curl -X 'POST' 'http://localhost:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{"username": "alice"}'
```
````

### Create a Post

```bash
curl -X 'POST' 'http://localhost:8000/posts/' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "My New Post",
  "content": "This is the content.",
  "tag": "tech"
}'
```

### Like a Post

```bash
curl -X 'POST' 'http://localhost:8000/users/1/like/5'
```

### Get Personalized Feed

**This is the main endpoint.**

```bash
curl 'http://localhost:8000/users/1/feed'
```

_Replace `1` with the ID of the user whose feed you want to see._

**Sample User IDs from seeded data:**

- **User Grace (id: 1):** Likes posts with tags **prayer, faith, and worship**.
- **User John (id: 2):** Likes posts with tags **bible, sermon, and outreach**.
- **User Hope (id: 3):** Likes posts with tags **hope and community**.

---

## Recommendation Method

**Method: Content-Based Filtering using Tags**

- The service uses **SQLite** as its lightweight, file-based database.
- Each post has a simple `tag` (e.g., "prayer", "sermon").
- To determine a user's preference, the system looks at all the tags of the posts they have liked.
- To generate a feed, all posts are scored. A post gets a score of `1` if its tag matches any of the user's liked tags, otherwise, it gets `0`.
- Posts are sorted by this score (highest first). Posts with the same score are sorted by ID (newest first, assuming auto-increment IDs).

**Trade-offs**

- binary scoring (1 for tag match, 0 otherwise) for easy implementation and understanding.

- New users receive posts in reverse chronological order. A real-world solution might use trending content or demographic-based recommendations.

---

## Error Handling

The API includes proper error handling for:

- Duplicate usernames (`400 Bad Request`)
- Non-existent users or posts (`404 Not Found`)
- Invalid request data (`422 Unprocessable Entity`)

---

## Testing

Run the comprehensive test suite with:

```bash
python -m pytest -v
```

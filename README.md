```markdown
# Personalized Feed API


**Live Demo:** https://humdov-interview.onrender.com

A simple FastAPI service that provides a personalized post feed based on user likes. It uses content-based filtering to determine user interests and serve relevant content.

---

## 🚀 Hosted Version

The API is successfully hosted on Render.com for easy testing:

**Base URL:** https://humdov-interview.onrender.com

**Interactive Documentation:** https://humdov-interview.onrender.com/docs

You're absolutely right! This crucial information should be in the README. Let's add a clear section for Windows users. Here's the updated README section:

## Update Your README.md

Add this section right after the "Quick Testing" part:

```markdown
### Seeding the Production Database

**For macOS/Linux (Bash):**
```bash
API_URL=https://humdov-interview.onrender.com python seed_data.py
```

**For Windows (PowerShell):**
```powershell
$env:API_URL="https://humdov-interview.onrender.com"; python seed_data.py
```

**For Windows (Command Prompt):**
```cmd
set API_URL=https://humdov-interview.onrender.com && python seed_data.py
```

**Alternative: Temporary code change**
You can also temporarily modify `seed_data.py`:
```python
# Change this line:
BASE_URL = "https://humdov-interview.onrender.com"  # For production
# Instead of:
# BASE_URL = "http://localhost:8000"  # For local development
```
Then run: `python seed_data.py`
```

## The updated "Hosted Version" section should look like:

```markdown
## 🚀 Hosted Version

The API is successfully hosted on Render.com for easy testing:

**Base URL:** https://humdov-interview.onrender.com

**Interactive Documentation:** https://humdov-interview.onrender.com/docs

### Quick Testing:

**First, seed the database:**
```bash
# macOS/Linux:
API_URL=https://humdov-interview.onrender.com python seed_data.py

# Windows PowerShell:
$env:API_URL="https://humdov-interview.onrender.com"; python seed_data.py

# Windows CMD:
set API_URL=https://humdov-interview.onrender.com && python seed_data.py
```

**Then test personalized feeds:**
```bash
curl https://humdov-interview.onrender.com/users/1/feed
curl https://humdov-interview.onrender.com/users/2/feed  
curl https://humdov-interview.onrender.com/users/3/feed
```

**Or use the interactive Swagger UI:**
- Visit: https://humdov-interview.onrender.com/docs
- Try the `/users/{user_id}/feed` endpoint with different user IDs
```

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
    pip install fastapi uvicorn sqlalchemy databases aiosqlite requests pytest httpx psycopg2-binary
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
    This will create 3 users and 10 faith-based posts, then assign likes to all 3 users.

**Sample User IDs from seeded data:**
- **User 1 (grace_believer):** Likes posts with tags **prayer, faith, and worship**.
- **User 2 (faith_journey):** Likes posts with tags **bible, sermon, and outreach**.
- **User 3 (hope_in_christ):** Likes posts with tags **hope and community**.

---

## Endpoints

### Create a User
```bash
curl -X 'POST' 'http://localhost:8000/users/' \
  -H 'Content-Type: application/json' \
  -d '{"username": "alice"}'
```

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
*Replace `1` with the ID of the user whose feed you want to see.*

---

## Recommendation Method

**Method: Content-Based Filtering using Tags**

- Each post has a simple `tag` (e.g., "prayer", "sermon").
- The system looks at all the tags of the posts a user has liked to determine their preference.
- To generate a user's feed, all posts are scored. A post gets a score of `1` if its tag matches any of the user's liked tags, otherwise it gets `0`.
- Posts are sorted by this score (highest first). Posts with the same score are sorted by ID (newest first, assuming auto-increment IDs).

**Trade-offs & Assumptions:**
- I straightforward content-based approach with binary scoring for easy implementation.
- I only considered explicit likes and single-post tags.
- New users receive posts in reverse chronological order.
- The current algorithm loads all posts into memory for scoring.

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

**Test coverage includes:**
- User creation (success and duplicate error cases)
- Personalized feed generation
- Error handling for non-existent users
- API endpoint validation
```
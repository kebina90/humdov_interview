import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")
print(f"Using API URL: {BASE_URL}")

def check_response(response, operation_name):
    if response.status_code >= 200 and response.status_code < 300:
        print(f"✓ Success: {operation_name}")
        return response.json()
    else:
        print(f"✗ Failed: {operation_name}")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def create_sample_data():
    print("Seeding database with sample data...")
    users = []
    posts = []

    # user
    user_data_list = [
        {"username": "Grace"},
        {"username": "John"},
        {"username": "Hope"}
    ]
    
    for user_data in user_data_list:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        user_result = check_response(response, f"Create user {user_data['username']}")
        if user_result:
            users.append(user_result)

    # posts
    post_data_list = [
        {"title": "The Power of Prayer", "content": "I've experienced amazing answers to prayer this week. God is faithful!", "tag": "prayer"},
        {"title": "Sunday Sermon Notes", "content": "Pastor's message on forgiveness really spoke to me today.", "tag": "sermon"},
        {"title": "Bible Study Tips", "content": "Here's what helps me get the most out of my daily Bible reading.", "tag": "bible"},
        {"title": "Worship Music Recommendations", "content": "These songs have been blessing my quiet time recently.", "tag": "worship"},
        {"title": "Christian Community Matters", "content": "Why fellowship with other believers is essential for spiritual growth.", "tag": "community"},
        {"title": "Dealing with Doubt", "content": "It's normal to have questions - here's how I work through mine.", "tag": "faith"},
        {"title": "Serving in Ministry", "content": "My experience volunteering in our church's children's ministry.", "tag": "ministry"},
        {"title": "Christian Marriage Advice", "content": "Biblical principles that have strengthened our relationship.", "tag": "relationships"},
        {"title": "Hope in Difficult Times", "content": "How my faith sustained me through recent challenges.", "tag": "hope"},
        {"title": "Evangelism Ideas", "content": "Practical ways to share your faith in everyday life.", "tag": "outreach"}
    ]

    for post_data in post_data_list:
        response = requests.post(f"{BASE_URL}/posts/", json=post_data)
        post_result = check_response(response, f"Create post '{post_data['title']}'")
        if post_result:
            posts.append(post_result)

    # likes
    likes = [
        (users[0]['id'], posts[0]['id']),
        (users[0]['id'], posts[5]['id']),
        (users[1]['id'], posts[2]['id']),
        (users[1]['id'], posts[1]['id']),
        (users[2]['id'], posts[8]['id']),
        (users[2]['id'], posts[4]['id']),
        (users[0]['id'], posts[3]['id']),
        (users[1]['id'], posts[9]['id']),
    ]

    for user_id, post_id in likes:
        response = requests.post(f"{BASE_URL}/users/{user_id}/like/{post_id}")
        check_response(response, f"User {user_id} like post {post_id}")

    print("\nSeeding complete!")
    print("\nSample User IDs to test the personalized feed:")
    for user in users:
        print(f"  User: {user['username']} (id: {user['id']})")

if __name__ == "__main__":
    create_sample_data()
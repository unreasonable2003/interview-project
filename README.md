# Machine Coding Round

Boilerplate setup for a Python machine coding round.

## Setup

1. Activate the virtual environment (provided one is created):
```bash
source venv/bin/activate
```

2. Run tests:
```bash
pytest
```

## REST APIs

### 1. Create Post
**POST** `http://127.0.0.1:8000/posts`

**Request Body:**
```json
{
  "user_id": "string",
  "media_link": "string",
  "caption": "string"
}
```

**Response (201 Created):**
```json
{
    "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
    "user_id": "string",
    "content": {
        "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
        "media_link": "string",
        "caption": "string",
        "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
    },
    "created_date_time": "2026-03-20T18:45:25.123456",
    "update_date_time": "2026-03-20T18:45:25.123456"
}
```

### 2. Get All Posts (Descending Order)
**GET** `http://127.0.0.1:8000/posts/recent`

*Supports cursor pagination via `?cursor=&limit=10`*

**Response (200 OK):**
```json
[
    {
        "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
        "user_id": "string1",
        "content": {
            "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
            "media_link": "string2",
            "caption": "string3",
            "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
        },
        "created_date_time": "2026-03-20T18:39:44.731115",
        "update_date_time": "2026-03-20T18:39:44.731121"
    }
]
```

### 3. Get User Specific Posts
**GET** `http://127.0.0.1:8000/users/{user_id}/posts`

*Supports cursor pagination via `?cursor=&limit=10`*

**Response (200 OK):**
*(Returns list of objects in the same format as above)*

### 4. Update Post
**PUT** `http://127.0.0.1:8000/posts/{post_id}`

**Request Body (Fields are optional):**
```json
{
  "media_link": "updated_string",
  "caption": "updated_string"
}
```

**Response (200 OK):**
```json
{
    "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
    "user_id": "string1",
    "content": {
        "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
        "media_link": "updated_string",
        "caption": "updated_string",
        "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
    },
    "created_date_time": "2026-03-20T18:39:44.731115",
    "update_date_time": "updated_timestamp"
}
```

### 5. Delete Post
**DELETE** `http://127.0.0.1:8000/posts/{post_id}`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Post deleted successfully"
}
```

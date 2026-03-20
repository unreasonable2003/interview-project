import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Posts REST API")


class ContentResponse(BaseModel):
    content_id: str
    media_link: str
    caption: str
    post_id: str

class PostResponse(BaseModel):
    id: str
    user_id: str
    content: ContentResponse
    created_date_time: datetime
    update_date_time: datetime

class CreatePostRequest(BaseModel):
    user_id: str
    media_link: str
    caption: str

class UpdatePostRequest(BaseModel):
    media_link: Optional[str] = None
    caption: Optional[str] = None

# In-memory database
posts_db: List[PostResponse] = []


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(req: CreatePostRequest):

    """Create: Allow users to add new posts."""
    
    post_id = str(uuid.uuid4())
    content_id = str(uuid.uuid4())
    
    content = ContentResponse(
        content_id=content_id,
        media_link=req.media_link,
        caption=req.caption,
        post_id=post_id
    )
    
    post = PostResponse(
        id=post_id,
        user_id=req.user_id,
        content=content,
        created_date_time=datetime.now(),
        update_date_time=datetime.now()
    )
    
    posts_db.append(post)
    return post

@app.get("/posts/recent", response_model=List[PostResponse])
def get_recent_posts(cursor: Optional[datetime] = None, limit: int = 10):

    """Retrieve a timeline of posts, sorted by recency (most recent first).
    Use `cursor` to paginate through older posts."""

    filtered_posts = [p for p in posts_db if not cursor or p.created_date_time < cursor]
    sorted_posts = sorted(filtered_posts, key=lambda p: p.created_date_time, reverse=True)
    return sorted_posts[:limit]

@app.get("/users/{user_id}/posts", response_model=List[PostResponse])
def get_user_posts(user_id: str, cursor: Optional[datetime] = None, limit: int = 10):

    """Retrieve posts for a single user, sorted by recency.
    Use `cursor` to paginate through older posts."""
    
    user_posts = [p for p in posts_db if p.user_id == user_id]
    filtered_posts = [p for p in user_posts if not cursor or p.created_date_time < cursor]
    sorted_user_posts = sorted(filtered_posts, key=lambda p: p.created_date_time, reverse=True)
    return sorted_user_posts[:limit]

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: str, req: UpdatePostRequest):

    """Update: Modify existing post content."""

    for post in posts_db:
        if post.id == post_id:
            if req.caption is not None:
                post.content.caption = req.caption
            if req.media_link is not None:
                post.content.media_link = req.media_link
            post.update_date_time = datetime.now()
            return post
            
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):

    """Delete: Remove posts from the system."""

    for i, post in enumerate(posts_db):
        if post.id == post_id:
            del posts_db[i]
            return {"success": True, "message": "Post deleted successfully"}
            
    return {"success": False, "message": "Post not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


## POST : http://127.0.0.1:8000/posts <- Create Post

#Request body
# {
#   "user_id": "string",
#   "media_link": "string",
#   "caption": "string"
# }

#Response body
# {
#     "id": "string",
#     "user_id": "string",
#     "content": {
#         "content_id": "string",
#         "media_link": "string",
#         "caption": "string",
#         "post_id": "string"
#     },
#     "created_date_time": "2026-03-20T18:45:25.123456",
#     "update_date_time": "2026-03-20T18:45:25.123456"
# }

#------------------------------------------------

## GET : http://127.0.0.1:8000/posts/recent <- All Posts in Descending Order

#Response body
# [
#     {
#         "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
#         "user_id": "string1",
#         "content": {
#             "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
#             "media_link": "string2",
#             "caption": "string3",
#             "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
#         },
#         "created_date_time": "2026-03-20T18:39:44.731115",
#         "update_date_time": "2026-03-20T18:39:44.731121"
#     }
# ]

#------------------------------------------------

## GET : http://127.0.0.1:8000/users/{user_id}/posts <- User Specific Posts in Descending Order

##Response body
# [
#     {
#         "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
#         "user_id": "string1",
#         "content": {
#             "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
#             "media_link": "string2",
#             "caption": "string3",
#             "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
#         },
#         "created_date_time": "2026-03-20T18:39:44.731115",
#         "update_date_time": "2026-03-20T18:39:44.731121"
#     }
# ]

#------------------------------------------------

## PUT : http://127.0.0.1:8000/posts/{post_id} <- Update Post

##Request body

# {
#   "media_link": "string",
#   "caption": "string"
# }

## Response

# {
#     "id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43",
#     "user_id": "string1",
#     "content": {
#         "content_id": "2003b7cf-7669-4093-be58-c2600f7882b6",
#         "media_link": "updated_string",
#         "caption": "updated_string",
#         "post_id": "bd02585e-44e7-473a-bb90-9a1bf24a3e43"
#     },
#     "created_date_time": "2026-03-20T18:39:44.731115",
#     "update_date_time": "2026-03-20T18:51:08.184610"
# }

#---------------------------------------------------

## DELETE : http://127.0.0.1:8000/posts/{post_id} <- Delete Post

##Response body

# {
#   "success": true,
#   "message": "Post deleted successfully"
# }








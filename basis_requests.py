import requests

print("welke post wil je zien?")
input_post = input(">")
r = requests.get(f"http://localhost:3000/posts/{input_post}")
json = r.json()
id = json["id"]
title = json["title"]
views = json["views"]
r2 = requests.get(f"http://localhost:3000/comments")

comments = r2.json()


print(f"Post {id}: {title} ({views} views)")
for comment in comments:
    if comment["postId"] == id:
        print(f"-  {comment['text']}")

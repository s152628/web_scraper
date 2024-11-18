import requests

print("Wat wil je doen?")
print("1: Een post aanmaken")
print("2: Een comment toevoegen aan een bestaande post")

input_choice = input(">")
if input_choice == "1":
    print("Wat is de id van de post?")
    input_id = input(">")
    r = requests.get(f"http://localhost:3000/posts/{input_id}")
    if r.status_code == 200:
        print("Deze post bestaat al")
    else:
        print("Wat is de titel van de post?")
        input_title = input(">")
        print("Hoeveel views heeft de post?")
        input_views = input(">")
        data = {"id": input_id, "title": input_title, "views": input_views}
        r = requests.post("http://localhost:3000/posts", json=data)
elif input_choice == "2":
    print("Wat is de id van de post waar je een comment aan wil toevoegen?")
    input_postId = input(">")
    r = requests.get(f"http://localhost:3000/posts/{input_postId}")
    if r.status_code == 200:
        print("Wat is de id van de comment?")
        input_id = input(">")
        r = requests.get(f"http://localhost:3000/comments/{input_id}")
        if r.status_code == 200:
            print("Deze comment bestaat al")
        else:
            print("Wat is de tekst van de comment?")
            input_text = input(">")
            data = {"id": input_id, "text": input_text, "postId": input_postId}
            r = requests.post("http://localhost:3000/comments", json=data)
    else:
        print("Deze post bestaat niet")

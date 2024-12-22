import httpx

users = [
    {
        "name": "random",
        "display_name": "random_name",
    },
    {
        "name": "john",
        "display_name": "johnDoex",
    },
    {
        "name": "samhan",
        "display_name": "samCarl",
    },
    {
        "name": "carlson",
        "display_name": "carlson@123"
    },
    {
        "name": "foobar",
        "display_name": "carlson@123"
    }
]
for user in users:
    response = httpx.post("http://localhost:8000/api/v1/users/create", json=user)
    print(response.json())

teams = ['A', 'B', 'C', 'D', 'E']
users = list(range(1, 6))

for i in range(len(teams)):
    data = {
        "name": f"team_{teams[i]}",
        "description": f"This is team {teams[i]}",
        "admin": users[i]
    }
    response = httpx.post("http://localhost:8000/api/v1/teams/create", json=data)
    print(response.json())
import env
import requests


def get_access_token(client_id: str, client_secret : str) -> str:
   
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json().get("access_token")


def get_users_info (token: str, client_id: str, login: str):
    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }
    params = {"login": login}

    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", None)
    response.raise_for_status()

    if not data:
        return None
    
    return data[0]


def get_total_followers (token: str, client_id: str, id: str ) -> int:
    url = "https://api.twitch.tv/helix/channels/followers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }

    params = {"broadcaster_id": id}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("total", 0)



CLIENT_SERCRET = env.CLIENT_SECRET
CLIENT_ID = env.CLIENT_ID

users = ["rubius", "mouredev", "asdadasd", "ibai"]
users_data = []
not_found_users = []

token = get_access_token(CLIENT_ID, CLIENT_SERCRET)

for username in users:

    user = get_users_info(token, CLIENT_ID, username)

    if user is None:
        not_found_users.append(username)
    else:
        followers = get_total_followers(token, CLIENT_ID, user["id"] )
        users_data.append({
            "username": username,
            "created_at": user["created_at"],
            "followers": followers
        })
    
sort_by_followers = sorted(users_data, key=lambda x: x["followers"], reverse = True)
sort_by_date = sorted(users_data, key=lambda x: x["created_at"], reverse = False)

print("Ranking por numero de seguidores: ")

for id, user, in enumerate(sort_by_followers, start = 1):
    print(f"{id} - {user["username"]}: {user["followers"]} seguidores.")


print("Ranking por antiguedad del canal: ")

for id, user, in enumerate(sort_by_date, start = 1):
    print(f"{id} - {user["username"]}: Creado el {user["created_at"]}")

if not_found_users:
    print("Usuarios no encontrados:")
    for user in not_found_users:
        print(user)
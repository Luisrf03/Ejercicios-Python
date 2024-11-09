import ens
import requests
import base64

CLIENT_ID = ens.CLIENT_ID
CLIENT_SECRET = ens.CLIENT_SECRET

def get_access_token() -> str:
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Error obteninedo el toke de Spotify. {response.json()}")
    
    return response.json().get("access_token")


def get_artists_id (token: str,name: str) -> str:
    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": name,
        "type": "artist",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception (
            f"Error en la busqueda del artista: {response.json()}"
        )
    
    results = response.json()
    if results ["artists"]["items"]:
        return results["artists"]["items"][0]["id"]


def get_artists_info (token: str, id: str):
    url = f"https://api.spotify.com/v1/artists/{id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception (
            f"Error en la busqueda de informacin del artista. {response.json()}"
        )
    
    results = response.json()

    return {
        "name": results["name"],
        "followers": results["followers"]["total"],
        "popularity": results["popularity"]
    }



token = get_access_token()

artists = ["OASIS","LINKIN PARK", "Miky Woodz", "Bad Bunny","Beny jr"]
artists_data = []

for artistsname in artists:
    
    artists_id = get_artists_id(token, artistsname)
    artists_data.append( get_artists_info(token, artists_id))


sort_by_popularity = sorted(artists_data, key=lambda x: x["popularity"], reverse=True)

print(f"{sort_by_popularity}\n")


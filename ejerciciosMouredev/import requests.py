import requests
import ens


def get_access_token(client_id: str, client_secret: str) -> str:
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get("access_token")


def get_artist_id_by_name(token: str, artist_name: str) -> str:
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1  # Limitar la búsqueda a un solo artista
    }

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()

    # Extraer el ID del primer artista encontrado
    artist_data = response.json()
    artists = artist_data.get('artists', {}).get('items', [])

    if artists:
        return artists[0]['id']  # Devolver el ID del primer artista encontrado
    else:
        return None


def get_bands_info(token: str, artist_id: str):
    url = "https://api.spotify.com/v1/artists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "ids": artist_id  # Usar el ID del artista
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Lanzar error si la respuesta es incorrecta
    return response.json().get("artists", None)


# Obtener el token de acceso
CLIENT_ID = ens.CLIENT_ID
CLIENT_SECRET = ens.CLIENT_SECRET

token = get_access_token(CLIENT_ID, CLIENT_SECRET)

# Lista de nombres de bandas a buscar
bands = ["Gambi"]
bands_data = []
bands_not_found = []

for band_name in bands:
    # Buscar el ID del artista por su nombre
    artist_id = get_artist_id_by_name(token, band_name)

    if artist_id is None:
        bands_not_found.append(band_name)  # Si no se encuentra el artista, agregar a la lista
    else:
        # Obtener la información del artista usando el ID
        band_info = get_bands_info(token, artist_id)

        if band_info:
            bands_data.append({
                "name": band_name,
                "followers": band_info[0].get("followers", {}).get("total", 0),
                "genres": band_info[0].get("genres", [])
            })

# Imprimir los resultados
print("Bandas encontradas:", bands_data)
print("Bandas no encontradas:", bands_not_found)

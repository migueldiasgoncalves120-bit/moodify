import random
from ytmusicapi import YTMusic

ytmusic = YTMusic()

def gerar_musicas(mood):

    mood = mood.lower()

    consultas = {
        "indie": [
            "indie rock 2010s",
            "indie alternative english",
            "indie pop international"
        ],
        "calma": [
            "lofi chill beats",
            "acoustic chill songs",
            "soft indie playlist"
        ],
        "triste": [
            "sad indie songs",
            "melancholic acoustic",
            "sad alternative 2015"
        ],
        "feliz": [
            "happy pop hits",
            "feel good indie",
            "dance pop 2020"
        ],
        "energia": [
            "rock hype songs",
            "trap energy 2022",
            "hip hop workout"
        ],
    }

    # Se o mood existir no dicionário
    if mood in consultas:
        busca = random.choice(consultas[mood])
    else:
        # se o usuário digitar algo aleatório
        busca = mood + " music playlist"

    resultados = ytmusic.search(busca, filter="songs", limit=40)

    random.shuffle(resultados)

    musicas = []
    titulos_vistos = set()

    for musica in resultados:
        titulo = musica["title"]
        artista = musica["artists"][0]["name"]

        # filtro simples anti-coisa-aleatória
        if len(titulo) < 60 and titulo not in titulos_vistos:
            titulos_vistos.add(titulo)

            musicas.append({
                "titulo": titulo,
                "artista": artista,
                "capa": musica["thumbnails"][-1]["url"]
            })

        if len(musicas) >= 15:
            break

    return musicas

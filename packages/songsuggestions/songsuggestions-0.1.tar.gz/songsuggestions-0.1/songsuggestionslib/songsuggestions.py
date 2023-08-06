import random

def generate_songs():
    songs = [
        "Bekhayali",
        "Baarish",
        "Ban Ja Rani",
        "Sun Saathiya",
        "Let me love you",
        "Gulaabo",
        "Soch na sake",
        "Girls like you",
        "Attention",
        "Tujhe Kitna Chahne lage",
    ]
    return random.choice(songs)

print(generate_songs())
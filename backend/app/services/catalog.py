"""
Curated fallback catalog.

When no Spotify API credentials are configured (or the Spotify API call
fails/rate-limits), the playlist builder falls back to this hand-picked,
genre-matched catalog so the product still works end-to-end out of the box.
Each entry mirrors the shape of a Spotify track object so the frontend
never has to special-case the source.
"""

CATALOG: dict[str, list[dict]] = {
    "happy": [
        {"title": "Walking on Sunshine", "artist": "Katrina & The Waves", "album": "Katrina & the Waves"},
        {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "album": "Uptown Special"},
        {"title": "Good as Hell", "artist": "Lizzo", "album": "Cuz I Love You"},
        {"title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "album": "Trolls"},
        {"title": "Happy", "artist": "Pharrell Williams", "album": "G I R L"},
        {"title": "Sunday Best", "artist": "Surfaces", "album": "Where the Light Is"},
        {"title": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia"},
        {"title": "Don't Stop Me Now", "artist": "Queen", "album": "Jazz"},
    ],
    "sad": [
        {"title": "Someone Like You", "artist": "Adele", "album": "21"},
        {"title": "Skinny Love", "artist": "Bon Iver", "album": "For Emma, Forever Ago"},
        {"title": "The Night We Met", "artist": "Lord Huron", "album": "Strange Trails"},
        {"title": "Liability", "artist": "Lorde", "album": "Melodrama"},
        {"title": "Hurt", "artist": "Johnny Cash", "album": "American IV"},
        {"title": "Fix You", "artist": "Coldplay", "album": "X&Y"},
        {"title": "Everybody Hurts", "artist": "R.E.M.", "album": "Automatic for the People"},
        {"title": "Falling", "artist": "Harry Styles", "album": "Fine Line"},
    ],
    "angry": [
        {"title": "Break Stuff", "artist": "Limp Bizkit", "album": "Significant Other"},
        {"title": "Killing in the Name", "artist": "Rage Against the Machine", "album": "Rage Against the Machine"},
        {"title": "Bulls on Parade", "artist": "Rage Against the Machine", "album": "Evil Empire"},
        {"title": "DUCKWORTH.", "artist": "Kendrick Lamar", "album": "DAMN."},
        {"title": "Given Up", "artist": "Linkin Park", "album": "Minutes to Midnight"},
        {"title": "Bodies", "artist": "Drowning Pool", "album": "Sinner"},
        {"title": "Bad Blood", "artist": "Bastille", "album": "Doom Days"},
        {"title": "HUMBLE.", "artist": "Kendrick Lamar", "album": "DAMN."},
    ],
    "neutral": [
        {"title": "Sunflower", "artist": "Post Malone & Swae Lee", "album": "Spider-Man: Into the Spider-Verse"},
        {"title": "Circles", "artist": "Post Malone", "album": "Hollywood's Bleeding"},
        {"title": "Cornerstone", "artist": "Arctic Monkeys", "album": "Humbug"},
        {"title": "Holocene", "artist": "Bon Iver", "album": "Bon Iver, Bon Iver"},
        {"title": "Best Part", "artist": "Daniel Caesar ft. H.E.R.", "album": "Freudian"},
        {"title": "Breathe", "artist": "Telepopmusik", "album": "Genetic World"},
        {"title": "Golden Hour", "artist": "JVKE", "album": "This Is What Ads Were Made For"},
        {"title": "La Vie en Rose", "artist": "Emily Watts", "album": "Piano Covers"},
    ],
    "fear": [
        {"title": "Weightless", "artist": "Marconi Union", "album": "Weightless"},
        {"title": "Breathe Me", "artist": "Sia", "album": "Colour the Small One"},
        {"title": "Haunted", "artist": "Beyoncé", "album": "Beyoncé"},
        {"title": "Bury a Friend", "artist": "Billie Eilish", "album": "When We All Fall Asleep"},
        {"title": "Clair de Lune", "artist": "Claude Debussy", "album": "Suite Bergamasque"},
        {"title": "Exit Music (For a Film)", "artist": "Radiohead", "album": "OK Computer"},
        {"title": "Anxiety", "artist": "Julia Michaels ft. Selena Gomez", "album": "Inner Monologue Pt. 1"},
        {"title": "Runaway", "artist": "AURORA", "album": "All My Demons Greeting Me as a Friend"},
    ],
    "surprise": [
        {"title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours"},
        {"title": "Bad Guy", "artist": "Billie Eilish", "album": "When We All Fall Asleep"},
        {"title": "One More Time", "artist": "Daft Punk", "album": "Discovery"},
        {"title": "Electric Feel", "artist": "MGMT", "album": "Oracular Spectacular"},
        {"title": "Titanium", "artist": "David Guetta ft. Sia", "album": "Nothing but the Beat"},
        {"title": "Instant Crush", "artist": "Daft Punk ft. Julian Casablancas", "album": "Random Access Memories"},
        {"title": "Feel It Still", "artist": "Portugal. The Man", "album": "Woodstock"},
        {"title": "I Bet You Look Good on the Dancefloor", "artist": "Arctic Monkeys", "album": "Whatever People Say I Am"},
    ],
    "disgust": [
        {"title": "Basket Case", "artist": "Green Day", "album": "Dookie"},
        {"title": "My Own Worst Enemy", "artist": "Lit", "album": "A Place in the Sun"},
        {"title": "Duality", "artist": "Slipknot", "album": "Vol. 3: The Subliminal Verses"},
        {"title": "American Idiot", "artist": "Green Day", "album": "American Idiot"},
        {"title": "Judith", "artist": "A Perfect Circle", "album": "Mer de Noms"},
        {"title": "Institutionalized", "artist": "Suicidal Tendencies", "album": "Suicidal Tendencies"},
        {"title": "Rise Against", "artist": "Rise Against", "album": "Siren Song of the Counter Culture"},
        {"title": "Nausea", "artist": "Beck", "album": "Modern Guilt"},
    ],
}


def get_catalog_tracks(emotion: str, limit: int = 10) -> list[dict]:
    tracks = CATALOG.get(emotion, CATALOG["neutral"])
    out = []
    for i, t in enumerate(tracks[:limit]):
        out.append({
            "id": f"catalog-{emotion}-{i}",
            "title": t["title"],
            "artist": t["artist"],
            "album": t.get("album"),
            "image": None,
            "preview_url": None,
            "external_url": f"https://open.spotify.com/search/{t['title'].replace(' ', '%20')}%20{t['artist'].replace(' ', '%20')}",
        })
    return out

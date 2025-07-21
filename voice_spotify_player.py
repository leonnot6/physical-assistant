import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr

# Replace these with your credentials
SPOTIPY_CLIENT_ID = '32fa50f4c0154802af23c5af0c5e2a90'
SPOTIPY_CLIENT_SECRET = 'cacce2027b3149b59f4fc3f7313b66d9'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'

# Set up Spotify authorization
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

# Set up speech recognition
recognizer = sr.Recognizer()

with sr.Microphone(sample_rate=16000) as source:
    print("Say the song name ")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    spoken = recognizer.recognize_google(audio)
    print(f"You said: {spoken}")

    # Extract song title and artist (if present)
    spoken_lower = spoken.lower()
    if " by " in spoken_lower:
        title, artist = map(str.strip, spoken_lower.split(" by ", 1))
    else:
        title = spoken_lower.strip()
        artist = ""

    print(f"Searching for: '{title}' by '{artist or 'any artist'}'")

    # Build search query
    if artist:
        query = f"track:{title} artist:{artist}"
    else:
        query = f"track:{title}"

    # Search for tracks
    results = sp.search(q=query, type='track', limit=10)

    # Try to match exact artist if specified
    track = None
    if artist:
        for item in results['tracks']['items']:
            result_artists = [a['name'].lower() for a in item['artists']]
            if artist.lower() in result_artists:
                track = item
                break

    # If no artist match or no artist provided, use top result
    if not track and results['tracks']['items']:
        track = results['tracks']['items'][0]

    # Play the track
    if track:
        track_uri = track['uri']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        print(f"Now playing: {track_name} by {artist_name}")
        sp.start_playback(uris=[track_uri])
    else:
        print("No matching track found on Spotify.")

except sr.UnknownValueError:
    print("Could not understand the audio.")
except sr.RequestError as e:
    print(f"Google STT error: {e}")
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API error: {e}")
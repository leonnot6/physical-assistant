import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr

# Replace these with your actual values
SPOTIPY_CLIENT_ID = '32fa50f4c0154802af23c5af0c5e2a90'
SPOTIPY_CLIENT_SECRET = 'cacce2027b3149b59f4fc3f7313b66d9'
SPOTIPY_REDIRECT_URI = 'https://127.0.0.1:8888/callback'

# Set up Spotify authorization
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    open_browser=True
))

# Set up speech recognition
recognizer = sr.Recognizer()

with sr.Microphone(sample_rate=16000) as source:
    print("🎤 Say the name of the song you want to play:")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    song_name = recognizer.recognize_google(audio)
    print(f"🔍 You said: {song_name}")

    if " by " in song_name.lower():
        title, artist = song_name.lower().split(" by ")
    else:
        title = song_name
        artist = ""

    results = sp.search(q=f"track:{title} artist:{artist}", type='track', limit=10)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_uri = track['uri']
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        print(f"🎶 Now playing: {track_name} by {artist_name}")
        sp.start_playback(uris=[track_uri])
    else:
        print("❌ Song not found on Spotify.")

except sr.UnknownValueError:
    print("❌ Could not understand audio.")
except sr.RequestError as e:
    print(f"⚠️ Google STT error: {e}")
except spotipy.exceptions.SpotifyException as e:
    print(f"⚠️ Spotify API error: {e}")
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
    print("Say a command like 'Play [song]', 'Pause', 'Resume', 'Skip', or 'Go back':")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    spoken = recognizer.recognize_google(audio)
    command = spoken.lower().strip()
    print(f"You said: {spoken}")

    # Extract song title and artist (if present)
    
    if "pause" in command:
        sp.pause_playback()
        print("⏸️ Paused playback.")

    elif "resume" in command or "continue" in command or "play music" in command:
        sp.start_playback()
        print("▶️ Resumed playback.")

    elif "skip" in command or "next" in command:
        sp.next_track()
        print("⏭️ Skipped to next track.")

    elif "go back" in command or "previous" in command or "back" in command:
        sp.previous_track()
        print("⏮️ Went to previous track.")

    elif "play" in command:
        # Try to extract "play [song] by [artist]"
        song_part = command.replace("play", "", 1).strip()

        if " by " in song_part:
            title, artist = map(str.strip, song_part.split(" by ", 1))
        else:
            title = song_part
            artist = ""

        print(f"🎵 Searching for: '{title}' by '{artist or 'any artist'}'")
        query = f"track:{title} artist:{artist}" if artist else f"track:{title}"

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
    else:
        print("Command not recognized.")

except sr.UnknownValueError:
    print("Could not understand the audio.")
except sr.RequestError as e:
    print(f"Google STT error: {e}")
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API error: {e}")
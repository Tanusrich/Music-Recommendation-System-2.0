import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

# Set up Spotify credentials
client_id = "1f84c74871cd40569b018340cee3c8ba"
client_secret = "eef32338be1b468191f7be906b7c0960"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(track_name):
    try:
        results = sp.search(q=track_name, type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']

            recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']
            return recommendations
        else:
            return None
    except Exception as e:
        st.error("Failed to fetch recommendations: {}".format(e))
        return None

st.title("Music Recommendation System")
track_name = st.sidebar.text_input("Enter a song name:")
submit = st.sidebar.button("Get Recommendations")

if submit and track_name:
    with st.spinner("Fetching recommendations..."):
        recommendations = get_recommendations(track_name)
        if recommendations:
            st.write("Recommended songs:")
            for track in recommendations:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(track['album']['images'][0]['url'], width=100)
                with col2:
                    st.write(f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
        else:
            st.error("No recommendations found. Try another song.")


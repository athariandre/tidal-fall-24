import subprocess

def download_spotify_playlist(playlist_url, output_dir):
    """
    Downloads a Spotify playlist using spotdl.

    :param playlist_url: URL of the Spotify playlist
    :param output_dir: Directory where the downloaded songs will be saved
    """
    command = [
        'spotdl',
        'download',
        playlist_url,
        '--output', output_dir
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    playlist_url = "https://open.spotify.com/playlist/4mPodK6ifH2VKsXj9a5JBs?si=dbn2iS4lQ2qKRYJ8OMRm0w"
    output_dir = "/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/audio_files"
    download_spotify_playlist(playlist_url, output_dir)
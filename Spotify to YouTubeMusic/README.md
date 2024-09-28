## Installation

1. Clone this repository:

   ```
   git clone https://github.com/CluxOP/Python.git
   cd Spotify to YouTubeMusic
   ```

2. Install required packages:

   ```
   pip install -r requirements.txt
   ```

   or

   ```
   pip install spotipy python-dotenv ytmusicapi
   ```

3. Set up your Spotify API credentials:

   - Create a `.env` file in the project root
   - Add your Spotify client ID and client secret:
     ```
     SPOTIFY_CLIENT_ID=your_client_id_here
     SPOTIFY_CLIENT_SECRET=your_client_secret_here
     ```

4. Set up YouTube Music authentication:
   - Run the following command and follow the prompts:
     ```
     ytmusicapi oauth
     ```
   - This will create an `oauth.json` file in your current directory

## Usage

1. First, ensure you've completed the YouTube Music authentication step:

   ```
   ytmusicapi oauth
   ```

2. Run the main script:

   ```
   python main.py
   ```

3. Follow the prompts to:
   - Select a Spotify playlist to transfer
   - Enter a name for the new YouTube Music playlist

The script will then create the playlist and add the songs it finds on YouTube Music.

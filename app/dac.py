import sys
import os
import argparse
import time
import discogs_client
import spotipy
import spotipy.util as util


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


DISCOGS_USER_TOKEN = os.environ["DISCOGS_USER_TOKEN"]
SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]
TIDAL_USERNAME = os.environ["TIDAL_USERNAME"]
TIDAL_PASSWORD = os.environ["TIDAL_PASSWORD"]


def convert_spotify():
    spotify_scope = 'user-library-read'
    spotify_token = util.prompt_for_user_token(SPOTIFY_USERNAME, spotify_scope)
    if not spotify_token:
        print("Could not authenticate with Spotify")
        sys.exit()
    spotify = spotipy.Spotify(auth=spotify_token)
    discogs = discogs_client.Client('DAC/0.1', user_token=DISCOGS_USER_TOKEN)
    not_found = []
    me = discogs.identity()

        spotify_results = spotify.current_user_saved_albums()
        # Grab all saved albums from user
        albums = spotify_results['items']
        while spotify_results['next']:
            spotify_results = spotify.next(spotify_results)
            albums.extend(spotify_results['items'])
        # Add saved albums to wantlist
        for album in albums:
            print(album['album']['name'] + ' - ' + album['album']['artists'][0]['name'])
            discogs_results = discogs.search(album['album']['name'], type='release', artist=album['album']['artists'][0]['name'])
            if discogs_results and discogs_results[0].artists[0].name == album['album']['artists'][0]['name']:
                me.wantlist.add(discogs_results[0].id)
            else:
                not_found.append(album['album']['name'] + ' - ' + album['album']['artists'][0]['name'])
                print('Album not found!')
            # sleep to throttle requests to Discogs
            time.sleep(3)
    print(bcolors.FAIL + "The following albums were not found:" + bcolors.ENDC)
    for nf in not_found:
        print(nf)


def convert_tidal():
    pass


def main():
    parser = argparse.ArgumentParser(description="Converts digital"
                                     "music libraries to Discogs wantlist")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--spotify",
                       help="convert from spotify saved albums",
                       action="store_true")
    group.add_argument("-t", "--tidal",
                       help="convert from tidal favorite albums",
                       action="store_true")
    args = parser.parse_args()

    if args.spotify:
        print(bcolors.OKGREEN +
              "Please wait as your saved albums are saved to your wantlist" +
              bcolors.ENDC)
        print("This will take a while due to Discogs limitations")
        convert_spotify()
    elif args.tidal:
        print(bcolors.OKBLUE +
              "Please wait as your favorite albums "
              "are saved to your wantlist" +
              bcolors.ENDC)
        print("This will take a while due to Discogs limitations")
        # convert_tidal()


if __name__ == "__main__":
    main()

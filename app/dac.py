import sys
import os
import argparse
import time
import re
import discogs_client
import spotipy
import spotipy.util as util
from tqdm import tqdm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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


def convert_spotify(nearness):
    added = []
    not_found = []
    wantlist = []
    choices = {}

    # set up Spotify API
    spotify_scope = 'user-library-read'
    spotify_token = util.prompt_for_user_token(SPOTIFY_USERNAME, spotify_scope)
    if not spotify_token:
        print("Could not authenticate with Spotify")
        sys.exit()
    spotify = spotipy.Spotify(auth=spotify_token)

    # set up Discogs API
    discogs = discogs_client.Client('DAC/0.1', user_token=DISCOGS_USER_TOKEN)
    # 100 results per page to minimize API call usage
    discogs._per_page = 100

    # Grab the user's current wantlist
    # Will decrease the amount of useless queries
    me = discogs.identity()
    num_pages = me.wantlist.pages
    for i in range(1, num_pages + 1):
        for want in me.wantlist.page(i):
            wantlist.append(want.release.artists[0].name.upper() + " - " + want.release.title.upper())

    # Grab all saved albums from user
    spotify_results = spotify.current_user_saved_albums()
    albums = spotify_results['items']
    while spotify_results['next']:
        spotify_results = spotify.next(spotify_results)
        albums.extend(spotify_results['items'])

    # Add saved albums to wantlist
    for album in tqdm(albums):
        album_name = re.sub('\(.*? Edition\)|\(.*? Version\)|\(Deluxe\)', '', album['album']['name'])
        # used for Discogs search
        # Strip non-numeric characters, remove parenthesis and their contents
        formatted_album_name = re.sub('[^ a-zA-Z0-9]', '', album_name)
        artist_name = album['album']['artists'][0]['name']
        title_name = artist_name + " - " + album_name

        if title_name.upper() not in wantlist:
            discogs_results = discogs.search(formatted_album_name, type='release')
            # If there are more than 2 pages of results, we need to narrow the search parameters
            if discogs_results.pages > 2:
                discogs_results = discogs_results = discogs.search(formatted_album_name, type='release', artist=artist_name)
            # Get the first 100 results (hopefully this is enough)
            for result in discogs_results.page(0):
                choices[result.title] = result.id
            # Get the closest matching result
            nearest = process.extractOne(title_name, choices.keys(), scorer=fuzz.token_sort_ratio)
            # Make sure the closest matching result meets our nearness parameter
            if nearest and nearest[1] > nearness:
                me.wantlist.add(choices[nearest[0]])
                added.append(nearest[0])
            else:
                not_found.append(title_name)
            choices = {}
            # sleep to throttle requests to Discogs
            time.sleep(3)

    # Let the user know what was added/not found
    if added:
        print(bcolors.OKGREEN + "The following albums were added to your wantlist:" +
              bcolors.ENDC)
        for a in added:
            print(a)

    if not_found:
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
    parser.add_argument("-n", "--nearness",
                        help="Level of nearness needed to match albums: 0 - 100",
                        action="store",
                        default=80)
    args = parser.parse_args()

    if args.spotify:
        print(bcolors.OKGREEN +
              "Please wait as your saved albums are saved to your wantlist" +
              bcolors.ENDC)
        print("This will take a while due to Discogs limitations")
        convert_spotify(args.nearness)
    elif args.tidal:
        print(bcolors.OKBLUE +
              "Please wait as your favorite albums "
              "are saved to your wantlist" +
              bcolors.ENDC)
        print("This will take a while due to Discogs limitations")
        # convert_tidal()


if __name__ == "__main__":
    main()

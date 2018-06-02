# dac
dac stands for Digital-to-Analog Converter, though not in the typical sense.
It allows you to convert your digital music libraries to a Discogs(analog) wantlist.
This is a rudimentary command-line client -- a web interface that will be much
easier to use is coming.

## Prerequisites
- Vagrant
- VirtualBox (or other Vagrant provider)

## Installing
```
vagrant up
```

## Services supported
- Spotify

## Services in progress
- Tidal
- Google Play

## How to use
- Rename docker-compose.yml.sample to docker-compose.yml
- Discogs
    - Generate a user-token from the
      [developer settings on the Discogs website](https://www.discogs.com/settings/developers)
    - Replace the DISCOGS_USER_TOKEN placeholder in the docker-compose file
- If using Spotify:
    - Create a new application and receive your client id and secret using the
    [developer dashboard on the Spotify website](https://developer.spotify.com/dashboard/applications)
    - Replace the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET placeholders
    in the docker-compose file
    - Add http://localhost as a Redirect URI in your application settings.
        - After logging in, you will copy the resulting Redirect URL and provide
        it to DAC
    - Replace the SPOTIPY_REDIRECT_URI placeholder with the Redirect URI you
    provided above
    - Replace the SPOTIFY_USERNAME placeholder with your Spotify username
- Run the command line client
    - SSH into the Vagrant box:

        ```
        vagrant ssh
        ```

    - Run bash in our Docker container

        ```
        docker exec -it vagrant_app_1 /bin/bash
        ```

    - Run the command-line client, specifying the service desired,
    and a nearness parameter, if the default of 80 is too strict/loose

        ```
        python dac.py (-s | -t) [-n]
        ```
- If any albums cannot be saved to your wantlist, they will listed after
all other albums have been added

## Notes
- Special editions/versions may be stripped
- Versions of albums not on Discogs will not be added
- Discogs is a user-submitted site, so some album/artists names may have
different symbols than in Spotify

## TODO:
- Allow users to specify which format they want to default to i.e. CD, 12"

## Built With
- [Discogs Python API](https://github.com/discogs/discogs_client) -
Official Discogs Python API
- [Spotipy](http://spotipy.readthedocs.io/en/latest/#) -
Spotify Python API
- [tidalapi](https://pythonhosted.org/tidalapi/#) -
Unofficial Tidal Python API
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - SeatGeek's fuzzy
string matching

## License
This project is licensed under the MIT license -
see the [LICENSE.md](LICENSE.md) for details
